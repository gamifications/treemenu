from django.db import models
from treebeard.mp_tree import MP_Node

from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (0, 'Others'), #admin, superadmin etc, so ./manage.py createsuperuser will return default
      (1, 'Shop Manager'),
      (2, 'Customer'),
      (3, 'Seller'),
      # (4, 'Secretary'),
      # (5, 'Supervisor'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,default=0)
class Category(MP_Node):
    name = models.CharField(max_length=30)
    node_order_by = ['name']
    def __str__(self):
        return 'Category: {}'.format(self.name)