from django.db import models
from treebeard.mp_tree import MP_Node

from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    
    user_type = models.ForeignKey('Usertype', on_delete=models.CASCADE, null=True)

class Usertype(models.Model):
    # USER_TYPE_CHOICES = (
    #   (0, 'Others'), #admin, superadmin etc, so ./manage.py createsuperuser will return default
    #   (1, 'Shop Manager'),
    #   (2, 'Customer'),
    #   (3, 'Seller'),
    #   # (4, 'Secretary'),
    #   # (5, 'Supervisor'),
    # )
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Category(MP_Node):
    user_type = models.ForeignKey('Usertype', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    node_order_by = ['name']
    def __str__(self):
        return 'Category: {}'.format(self.name)