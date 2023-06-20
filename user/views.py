from django.shortcuts import render,redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .import forms
# Create your views here.
def profiles(request):
    profile=Profile.objects.all()
    return render(request,'user/profiles.html',{'profiles':profile})
def profile(request,uid):
    profile=Profile.objects.get(id=uid)
    topSkill=profile.skills_set.exclude(description__exact='')
    otherSkill=profile.skills_set.filter(description='')
    return render(request,'user/user-profile.html',{'profile':profile,'topskill':topSkill,'otherskill':otherSkill})


def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('profiles')


    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exist')
        

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("index")
        else:
            messages.error(request,'Username or password is incorrect !')    
    return render(request,'user/login_register.html',{'page':page})        

def logOut(request):
    logout(request)
    messages.error(request,'User was logged out successfully !')  
    return redirect('login')

def register(request):
    page='register'
    form=forms.CustomUserForm()
    context={'page':page,'form':form}

    if request.method=='POST':
        form=forms.CustomUserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            messages.success(request,"User was created")
            return redirect('index')
        else:
            messages.error(request,"Error Occured")




    return render(request,'user/login_register.html',context)
@login_required(login_url='login')
def userAccount (request):
    user=request.user.Profile


    context={'profile':user}
    return render(request,"user/account.html",context)