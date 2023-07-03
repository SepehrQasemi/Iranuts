from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from Shop.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import CustomUserManager


class CustomUser (AbstractUser):
    phone = models.CharField(unique=True,null=False,blank=False,max_length=13,validators=[
        RegexValidator(
            
        regex=r'^\+?1?\d{11,11}$',
        message="Phone number must be in the format: '0999999999'. Up to 11 digits allowed."
        )
    ])
    email = models.CharField(max_length=254,null=True,blank=True)
    # province = models.ForeignKey(Province,on_delete=models.SET_NULL,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return str(self.phone)
    
    
    objects = CustomUserManager()

@receiver(post_save,sender=CustomUser)
def addCart (sender,instance,created,**kwargs):
    if created:
        cart=Cart(user=instance)
        cart.save()

