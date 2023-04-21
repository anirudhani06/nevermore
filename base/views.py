from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .forms import ProjectForm,CommentForm
from .models import Projects,Tag,Comments
from .utils import search_developers,search_projects

# Create your views here.

@login_required(login_url='login')
def home(request):
    all_developers = search_developers(request)
    p = Paginator(all_developers,6)
    page = request.GET.get('page')
    developers = p.get_page(page)
    num_pages = developers.paginator.page_range
    developers_count = all_developers.count()
    
    context = {'dev':developers,'num_pages':num_pages,'developers_count':developers_count}
    return render(request,'base/home.html',context)

@login_required(login_url='login')
def all_projects(request):
    all_projects = search_projects(request)

    p = Paginator(all_projects,6)
    page = request.GET.get('page')
    projects = p.get_page(page)
    num_pages =projects.paginator.page_range

    project_count = all_projects.count()

    context = {'projects':projects,'num_pages':num_pages,'project_count':project_count}
    return render(request,'base/projects.html',context)

@login_required(login_url='login')
@csrf_exempt
def project(request,project_id):
    project = Projects.objects.get(id=project_id)
    form = CommentForm()
    comments = Comments.objects.filter(project=project)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.owner = request.user.profile
            comment.project = project
            comment.save()

    context = {'project':project,'form':form,'comments':comments}
    return render(request,'base/project.html',context)

@login_required(login_url='login')
@csrf_exempt
def add_project(request):
    form = ProjectForm()

    if request.method == "POST":
        tags = request.POST.get('tags').replace(',',' ').split()

        title = request.POST.get('title').title()
        project = Projects.objects.create(
            owner = request.user.profile,
            image = request.FILES['image'],
            title = title,
            sourceCode = request.POST.get('sourceCode'),
            body = request.POST.get('body')
        )

        for tag_name in tags:
            tag,created = Tag.objects.get_or_create(name=tag_name)
            project.tags.add(tag)
            
        return redirect('my-account')

    context = {'form':form}
    return render(request,'base/create_project.html',context)

@login_required(login_url='login')
@csrf_exempt
def update_project(request,project_id):
    project = Projects.objects.get(id=project_id)
    if project.owner != request.user.profile:
        return HttpResponse('you cant update this post!')
    
    form = ProjectForm(instance=project)
    tags = ''

    for i,tag in enumerate(project.tags.all()):
        if i <= len(project.tags.all())-2:
            tags += f"{tag},"
        else:
            tags += f"{tag}"
    
    if request.method == "POST":
        try:
            project.image = request.FILES['image']
        except:
            project.image = project.image
        
        project.title = request.POST.get('title')
        project.sourceCode = request.POST.get('sourceCode')
        project.body = request.POST.get('body')
        for tag in project.tags.all():
            project.tags.remove(tag)
        project.save()

        new_tags = request.POST.get('tags').replace(',',' ').split()

        for tag_name in new_tags:
            tag,created= Tag.objects.get_or_create(name=tag_name)
            project.tags.add(tag)

        return redirect('my-account')

    context = {'project':project,'form':form,'tags':tags}
    return render(request,'base/update_project.html',context)

@login_required(login_url='login')
@csrf_exempt
def delete_project(request):
    if request.method == "POST":
        project_id = request.POST.get('id')
        project = Projects.objects.get(id=project_id)

        if project.owner == request.user.profile:
            project.delete()
        else:
            return HttpResponse('You cant delete this post!')
        
        all_projects = Projects.objects.filter(owner = request.user.profile)

        
        return JsonResponse({
            'projects':all_projects
        })

@login_required(login_url='login')
@csrf_exempt
def like(request):
    if request.method == "POST":
        project = Projects.objects.get(id=request.POST.get('id'))

        if not project.likes.filter(id=request.user.profile.id).exists():
            project.likes.add(request.user.profile.id)
            project.dislikes.remove(request.user.profile.id)
            project.total_likes = project.likes.count() + project.dislikes.count()
            project.save()

            project.positive_feedback
            feedback = project.feedback
         
        
        return JsonResponse({
            'likes':project.total_likes,
            'feedback':feedback,
        })

@login_required(login_url='login')
@csrf_exempt
def dislike(request):
    if request.method == "POST":
        project = Projects.objects.get(id=request.POST.get('id'))

        if not project.dislikes.filter(id=request.user.profile.id).exists():
            project.dislikes.add(request.user.profile.id)
            project.likes.remove(request.user.profile.id)
            project.total_likes = project.likes.count() + project.dislikes.count()
            project.save()

            project.positive_feedback
            feedback = project.feedback
        return JsonResponse({
            'likes':project.total_likes,
            'feedback':feedback,
        })
