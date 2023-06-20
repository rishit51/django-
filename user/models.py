from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,blank=True,null=True)
    email=models.EmailField(blank=True,null=True)
    location=models.CharField(max_length=200,null=True,blank=True)
    short_intro=models.CharField(max_length=200,blank=True,null=True)
    bio=models.TextField(null=True,blank=True)
    Profile_img=models.ImageField(null=True,blank=True,upload_to='profiles',default='profiles/default.png')
    github=models.CharField(max_length=200,blank=True,null=True)
    linkedin=models.CharField(max_length=200,blank=True,null=True)
    youtube=models.CharField(max_length=200,blank=True,null=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.name
class Skills(models.Model):
    owner=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,blank=True,null=True)
    description=models.TextField(null=True,blank=True)   
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    created=models.DateTimeField(auto_now_add=True )

    
    def __str__(self):
        return self.name 

# post_save.connect(profileUpdated,Profile)
# post_delete.connect(deleteUser,Profile)        