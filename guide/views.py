from django.shortcuts import render, redirect
from django.contrib import messages

from guide.models import Category

# Create your views here.
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
