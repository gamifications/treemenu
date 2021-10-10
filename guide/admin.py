from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .models import Usertype, Category # , Article


admin.site.unregister(Group)
# admin.site.register(Article)
admin.site.register(Usertype)

class CustUserAdmin(UserAdmin):
    search_fields = ('username', )
    fieldsets = (
        (None, {'fields': ('username','email', 'password', 'first_name', 'last_name','user_type')}),
        )
admin.site.register(get_user_model(), CustUserAdmin)

class CategoryAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
# admin.site.register(Category, CategoryAdmin)
