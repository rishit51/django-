from django.shortcuts import render,redirect
from .forms import ProjectForm
from .models import Project
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def index(request):
    projects=Project.objects.all()
    msg='Hello this is a message'
    return render(request,'projects/projects.html',{'msg':msg,'projects':projects})
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
            form.save()
            return redirect('index')
    context={'form':form}
    return render(request,'projects/project_form.html',context)

def updateProject(request,pk):
    form=ProjectForm(instance=Project.objects.get(id=pk))

    if request.method=='POST':
        form=ProjectForm(request.POST,request.FILES,instance=Project.objects.get(id=pk))
        if form.is_valid():
            form.save()
            return redirect('index')
    context={'form':form}
    return render(request,'projects/project_form.html',context)

def delProject(request,pk):
    project=Project.objects.get(id=pk)

    if request.method=='POST':
            project.delete()
            return redirect('index')
    
    context={'project':project}
    return render(request,'projects/delete.html',context)