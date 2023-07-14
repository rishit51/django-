from .models import Profile, Skills
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(request, projects, results):
    pages = request.GET.get('page', 1)  # Use a default value if 'page' parameter is not provided

    paginator = Paginator(projects, results)
    try:
        projects = paginator.page(pages)
    except PageNotAnInteger:
        pages = 1
        projects = paginator.page(pages)
    except EmptyPage:
        pages = paginator.num_pages
        projects = paginator.page(pages)

    left_index = max(1, int(pages) - 4)
    right_index = min(int(pages) + 5, paginator.num_pages)
    custom_range = range(left_index, right_index + 1)

    return custom_range, projects


def searchProfiles(request):
    search_query = ""

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skills.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skills__in=skills)
    )

    return profiles, search_query
