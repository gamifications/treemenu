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
    user_type = request.user.user_type
    context = {}
    if request.user.is_superuser:
        # print('super user')
        
        context['user_types'] = Usertype.objects.all()
        user_type = context['user_types'].first()
        if 'user_type' in request.GET:
            user_type= Usertype.objects.get(id=request.GET['user_type'])
            print('usertype', user_type)
    if pk:
        context['article_obj'] = Article.objects.get(pk=pk)
        if request.user.is_superuser:
            context['form'] = ArticleForm(instance=context['article_obj'])
    if request.method == 'POST':
        print(user_type)
        # if not request.user.user_type:
        #     messages.error(request, 'Error: User is not associated with any usertypes.')
        if request.POST.get('parent_id') and request.POST.get('category_name'):
            parent = request.POST['parent_id']
            cat = request.POST['category_name']
            is_cat = False if request.POST['cat_type'] == 'article' else True
            if parent=='0':
                Category.add_root(name=cat, user_type=user_type, is_category=is_cat)
            else:
                
                obj = Category.objects.get(pk=parent).add_child(
                    name=cat, user_type=user_type, is_category=is_cat)
                
                if not is_cat:
                    context['form'] = ArticleForm(instance=Article.objects.create(category=obj))
                
            messages.success(request, f'Success: Category {cat} created successfully.')
        else:
            messages.error(request, 'Error: Name is required.')
        return redirect('home')
    print('successs')
    context['user_type'] = user_type
    context['alist'] = Category.get_annotated_list_qs(Category.objects.filter(user_type=user_type))
    # cat_list = Category.get_annotated_list()
    return render(request,'home.html',context) #[c for c in cat_list if c[0].user_type == request.user.user_type]})

@login_required
def save_article(request):
    print(request.POST)
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