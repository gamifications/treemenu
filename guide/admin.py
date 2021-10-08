from django.contrib import admin
from django.contrib.auth import get_user_model
# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import Usertype, Category
class CustUserAdmin(UserAdmin):
    search_fields = ('username', )
    fieldsets = (
        (None, {'fields': ('username','email', 'password', 'first_name', 'last_name','user_type')}),
        )
admin.site.register(get_user_model(), CustUserAdmin)

admin.site.register(Usertype)
admin.site.register(Category)
