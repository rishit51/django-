from django.shortcuts import render,redirect
from .forms import ProjectForm
from .models import Project,Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

# Create your views here.

def index(request):
    search_query=""

    if request.GET.get('search_query'):
        search_query=request.GET.get('search_query')
    tags=Tag.objects.filter(name=search_query)    

    projects=Project.objects.distinct().filter(Q(title__icontains=search_query)|Q(description__icontains=search_query)|Q(owner__name__icontains=search_query)|Q(tags__in=tags))    
    return render(request,'projects/projects.html',{'search_query':search_query,'projects':projects})
def project(request,pk):
    project=Project.objects.get(id=pk)
    tag=project.tags.all()
    return render(request,'projects/single-project.html',{'project':project,'tag':tag})
@login_required(login_url='login')
def createProject(request):
    form=ProjectForm()


    if request.method=='POST':
        form=ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.owner=request.user.profile
            form.save()
            return redirect('index')
    context={'form':form}
    return render(request,'projects/project_form.html',context)
@login_required(login_url='login')
def updateProject(request,pk):
    project=request.user.profile.project_set.get(id=pk)
    form=ProjectForm(instance=project)

    if request.method=='POST':
        form=ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('index')
    context={'form':form}
    return render(request,'projects/project_form.html',context)
@login_required(login_url='login')
def delProject(request,pk):
    project=request.user.profile.project_set.get(id=pk)

    if request.method=='POST':
            project.delete()
            return redirect('index')
    
    context={'project':project}
    return render(request,'projects/delete.html',context)