from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from guide.models import Article, Category, Article, Usertype

from django.forms import ModelForm
class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'desc','id']


# Create your views here.
@login_required
def home(request, pk=None):
            
    if request.method == 'POST':
        if request.POST.get('parent_id') and request.POST.get('category_name'):
            # we take usertype from hidden input field
            user_type = Usertype.objects.get(id=request.POST['user_type'])
            parent = request.POST['parent_id']
            cat = request.POST['category_name']
            is_cat = False if request.POST['cat_type'] == 'article' else True
            if parent=='0':
                # if root category.
                # root category can be category or article
                Category.add_root(name=cat, user_type=user_type, is_category=is_cat)
            else:
                obj = Category.objects.get(pk=parent).add_child(
                    name=cat, user_type=user_type, is_category=is_cat)
                if not is_cat:
                    # create an empty article under category
                    Article.objects.create(category=obj)
                    # context['form'] = ArticleForm(instance=Article.objects.create(category=obj))
                
            messages.success(request, f'Success: Category {cat} created successfully.')
        else:
            messages.error(request, 'Error: Name is required.')
        return redirect('home')


    context = {}
    if pk:
        # if article
        context['article_obj'] = Article.objects.get(pk=pk)
        if request.user.is_superuser: context['form'] = ArticleForm(instance=context['article_obj'])

    if request.user.is_superuser:
        # we need all user_types to show it in the dropdown
        context['user_types'] = Usertype.objects.all()
        if 'user_type' in request.GET:
            context['user_type'] = Usertype.objects.get(id=request.GET['user_type'])
        else:
            context['user_type'] = context['user_types'].first()
    else:
        # if not an admin user user_type is current users user_type
        context['user_type'] = request.user.user_type
    
    # get all categories for a user_type
    context['alist'] = Category.get_annotated_list_qs(Category.objects.filter(user_type=context['user_type']))
    return render(request,'home.html',context)


@method_decorator([login_required], name='dispatch')
class Home(View):
    def get(self, request, articlepk=None):
        context = {}
        

        if request.user.is_superuser:
            # we need all user_types to show it in the dropdown
            context['user_types'] = Usertype.objects.all()
            if 'user_type' in request.GET:
                context['user_type'] = Usertype.objects.get(id=request.GET['user_type'])
            else:
                # if articlepk:
                #     # if article, set user_type as article's user_type
                #     context['user_type'] = 
                # else:
                context['user_type'] = context['user_types'].first()
        else:
            # if not an admin user user_type is current users user_type
            context['user_type'] = request.user.user_type
        
        if articlepk:
            # if article
            context['article_obj'] = Article.objects.get(pk=articlepk)
            if request.user.is_superuser: 
                context['form'] = ArticleForm(instance=context['article_obj'])

                # if article, set user_type as article's user_type
                context['user_type'] = context['article_obj'].category.user_type
        
        # get all categories for a user_type
        context['alist'] = Category.get_annotated_list_qs(Category.objects.filter(user_type=context['user_type']))
        return render(request,'home.html',context)

    def post(self,request):
        """Create New Category"""

        # we take usertype from hidden input field
        user_type = Usertype.objects.get(id=request.POST['user_type'])
        if request.POST.get('parent_id') and request.POST.get('category_name'):
            parent = request.POST['parent_id']
            cat = request.POST['category_name']
            is_cat = False if request.POST['cat_type'] == 'article' else True
            if parent=='0':
                # if root category.
                # root category can be category or article
                Category.add_root(name=cat, user_type=user_type, is_category=is_cat)
            else:
                obj = Category.objects.get(pk=parent).add_child(
                    name=cat, user_type=user_type, is_category=is_cat)
                if not is_cat:
                    # create an empty article under category
                    Article.objects.create(category=obj)
            messages.success(request, f'Success: Category {cat} created successfully.')
        else:
            messages.error(request, 'Error: Name is required.')
        return redirect(f"{reverse('home')}?user_type={user_type.pk}")

@login_required
def save_article(request):
    obj = Article.objects.get(pk= request.POST['articlepk'])
    obj.title = request.POST['title']
    obj.desc = request.POST['desc']
    obj.save()
    messages.success(request, f'Success: Article updated successfully.')
    return redirect(reverse('article', kwargs={"pk": obj.id})) #, args=(None,)) #,args=(1,))

@method_decorator([login_required], name='dispatch')
class Profile(View):
    # even inactive users can view/edit their profile
    def get(self, request):
        return render(request,'registration/profile.html')

    def post(self,request):
        # user_id=request.POST['user']
        user = request.user #User.objects.get(id = user_id)

        username = request.POST.get('username', '')
        if len(username) < 3:
            messages.error(request, 'Error: Username must have atleast 3 characters.')
            return redirect('profile')

        if username != user.username:
            if get_user_model().objects.filter(username=username).exists():
                messages.error(request, 'Error: Username already exists.')
                return redirect('profile')
            user.username = username    

        
        user.first_name = request.POST.get('first_name','')
        # user.last_name = request.POST.get('last_name', '')
        # user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, 'User details of {} saved with success!'.format(user.username))
        return redirect('profile')