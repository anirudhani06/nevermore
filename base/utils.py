from django.db.models import Q
from .models import Projects
from account.models import Profile

def search_developers(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    developers = Profile.objects.filter(Q(name__icontains=q) & Q(user__is_active=True))

    skill = request.GET.get('skill')

    if skill != None:
        p = Profile.objects.filter(Q(skills__name__icontains=skill))
        return p
    else:
        return developers

def search_projects(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    projects = Projects.objects.filter(Q(title__icontains=q))

    tag = request.GET.get('tag')

    if tag != None:
        p = Projects.objects.filter(tags__name__icontains=tag)
        
        return p
    else:
        return projects