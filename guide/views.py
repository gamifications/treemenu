from django.shortcuts import render

from django.contrib import messages

from guide.models import Category

# Create your views here.
def home(request):
    if request.method == 'POST':
        messages.warning(request, 'Saved Success fulley')

    return render(request,'home.html',{'menus':Category.dump_bulk(),'alist': Category.get_annotated_list()})