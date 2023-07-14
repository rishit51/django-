from django.shortcuts import render, redirect
from .forms import ProjectForm,reviewForm
from .models import Project, Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .utils import searchProfiles, paginateProjects

# Create your views here.


def index(request):
    projects, search_query = searchProfiles(request)

    [custom_range, projects] = paginateProjects(request, projects, 3)

    print(custom_range)

    return render(request, 'projects/projects.html', {'search_query': search_query, 'projects': projects, 'custom_range': custom_range})


def project(request, pk):
    project = Project.objects.get(id=pk)
    tag = project.tags.all()
    form=reviewForm()
    print(project.vote_ratio)
    if request.method=='POST':
        form=reviewForm(request.POST)
        review=form.save(commit=False)
        review.project=project
        review.owner=request.user.profile
        review.save()
        project.getVote
        messages.success(request,"Review saved")
        
        return redirect('single-project',pk=project.id)

    return render(request, 'projects/single-project.html', {'project': project, 'tag': tag,'form':form})


@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user.profile
            form.save()
           
            return redirect('index')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def updateProject(request, pk):
    project = request.user.profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delProject(request, pk):
    project = request.user.profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('index')

    context = {'project': project}
    return render(request, 'projects/delete.html', context)
