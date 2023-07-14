from django.shortcuts import render, redirect
from .models import Profile, Skills,Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .import forms
from django.db.models import Q
from .utils import searchProfiles, paginateProjects
# Create your views here.


def profiles(request):

    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProjects(request, profiles, 3)
    print(profiles.has_other_pages())
    return render(request, 'user/profiles.html', {'profiles': profiles, 'search': search_query, 'custom_range': custom_range})


def profile(request, uid):
    profile = Profile.objects.get(id=uid)
    topSkill = profile.skills_set.exclude(description__exact='')
    otherSkill = profile.skills_set.filter(description='')
    return render(request, 'user/user-profile.html', {'profile': profile, 'topskill': topSkill, 'otherskill': otherSkill})


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET['next'])
            else:
                return redirect('index')
        else:
            messages.error(request, 'Username or password is incorrect !')
    return render(request, 'user/login_register.html', {'page': page})


def logOut(request):
    logout(request)
    messages.error(request, 'User was logged out successfully !')
    return redirect('login')


def register(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit-account')

        else:
            messages.error(
                request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'user/login_register.html', context)


@login_required(login_url='login')
def createSkill(request):
    form = forms.SkillForm()

    if request.method == "POST":
        form = forms.SkillForm(request.POST)
        profile = request.user.profile
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill added succesfully !")
            return redirect('account')

    context = {'form': form}
    return render(request, "user/skill_form.html", context)


@login_required(login_url='login')
def updateSkill(request, pk):

    profile = request.user.profile
    skill = profile.skills_set.get(id=pk)
    form = forms.SkillForm(instance=skill)

    if request.method == "POST":
        form = forms.SkillForm(request.POST, instance=skill)
        profile = request.user.profile
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated succesfully !")
            return redirect('account')

    context = {'form': form}
    return render(request, "user/skill_form.html", context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skills_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects, }
    return render(request, 'user/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    form = forms.ProfileForm(instance=request.user.profile)
    context = {'form': form}

    if request.method == "POST":
        form = forms.ProfileForm(
            request.POST, request.FILES, instance=request.user.profile,)
        if form.is_valid():
            form.save()

            return redirect('account')

    return render(request, 'user/profile_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    Skill = profile.skills_set.get(id=pk)
    if request.method == "POST":
        Skill.delete()
        return redirect("account")

    return render(request, 'delete.html')

@login_required(login_url='login')
def message(request,id):
    profile=request.user.profile
    message=profile.messages.get(id=id)
    if not message.is_read:
        print('read message:'+str(message.is_read))
        message.is_read=True
        message.save()
        print(message.is_read)


    context={'message':message}
    return render(request,'user/message.html',context)

@login_required(login_url='login')
def inbox(request):
    profile=request.user.profile
    messageRequest=profile.messages.all()
    unreadCount=messageRequest.filter(is_read=False).count()
    context={'messageRequest':messageRequest,'unread':unreadCount}
    return render(request,'user/inbox.html',context)

def createMessage(request,pk):
    form=forms.messageForm()
    context={'profile':pk,'form':form}

    reciever=profile

    if request.method=='POST':
        try:
            sender=request.user.profile
        except:
            sender=None
               
        form=forms.messageForm(request.POST)
        if form.is_valid():
            message=form.save(commit=False)
            message.sender=sender
            message.recepient=Profile.objects.get(id=pk)
            if sender:
                message.name=sender.name
                message.email=sender.email
            message.save()
            messages.success(request,"Your message was sent")
            return redirect('profile',pk)    
    

    return render(request,'user/message_form.html',context)