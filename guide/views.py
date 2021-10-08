from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from django.contrib import messages
from django.contrib.auth import get_user_model
from guide.models import Category

# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        if request.POST.get('parent_id') and request.POST.get('category_name'):
            parent = request.POST['parent_id']
            cat = request.POST['category_name']
            if parent=='0':
                Category.add_root(name=cat)
            else:
                Category.objects.get(pk=parent).add_child(name=cat)
            messages.success(request, f'Success: Category {cat} created successfully.')
        else:
            messages.error(request, 'Error: Both Parent and Category Name is required.')
        return redirect('home')
    return render(request,'home.html',{'menus':Category.dump_bulk(),'alist': Category.get_annotated_list()})


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