from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(request, projects, results):
    pages = request.GET.get('page')

    paginator = Paginator(projects, results)
    try:
        projects = paginator.page(pages)
    except PageNotAnInteger:
        pages = 1
        projects = paginator.page(pages)
    except EmptyPage:
        pages = paginator.num_pages
        projects = paginator.page(pages)
    leftindex = int(pages)-4
    if leftindex < 1:
        leftindex = 1
    rightindex = (int(pages)+5)
    if rightindex > paginator.num_pages:
        rightindex = paginator.num_pages
    custom_range = range(leftindex, rightindex+1)

    projects = paginator.page(pages)

    return custom_range, projects


def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(Q(title__icontains=search_query) | Q(
        description__icontains=search_query) | Q(owner__name__icontains=search_query) | Q(tags__in=tags))

    return projects, search_query
