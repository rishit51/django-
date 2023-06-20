from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from django.db import models
from django.contrib.auth.models import User
from . import models
@receiver(post_save,sender=User)    
def createProfile(sender,instance,created,**kwargs):
    if created:
        user=instance
        profile=models.Profile.objects.create(user=user,email=user.email,name=user.first_name,username=user.username)
@receiver(post_delete,sender=models.Profile)
def deleteUser(sender,instance,**kwargs):
    user=instance.user
    user.delete()

@receiver(post_save,sender=models.Profile)
def updateUser(sender,instance,created,**kwargs):  
    profile=instance
    user=profile.user
    if not created:
        user.first_name=profile.name

        user.email=profile.email
        user.save()
        print(f"User changed: {user}")




