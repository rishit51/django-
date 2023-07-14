from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile ,Skills,Message


class CustomUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','email','username','password1','password2']
        labels={'first_name':'Name'}
        def __init__(self,*args, **kwargs):
            super(CustomUserForm,self).__init__(*args, **kwargs)

            for name,field in self.fields.items():
                field.widget.attrs.update({'class':'input'})



class ProfileForm(ModelForm):
    class Meta:
        model=Profile
        fields="__all__"

        def __init__(self,*args, **kwargs):
            super(ProfileForm,self).__init__(*args, **kwargs)

            for name,field in self.fields.items():
                field.widget.attrs.update({'class':'input'})
class SkillForm(ModelForm):
    
    class Meta:
        model=Skills
        exclude=["owner"]

        def __init__(self,*args, **kwargs):
            super(ProfileForm,self).__init__(*args, **kwargs)

            for name,field in self.fields.items():
                field.widget.attrs.update({'class':'input'})
        
class messageForm(ModelForm):
    class Meta:
        model=Message
        fields=['name','email','subject','body']

        def __init__(self,*args, **kwargs):
            super(messageForm,self).__init__(*args, **kwargs)

            for name,field in self.fields.items():
                field.widget.attrs.update({'class':'input'})


