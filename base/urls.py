from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),

    path('projects',views.all_projects,name='projects'),
    path('project/<str:project_id>',views.project,name='project'),
    
    path('add-project',views.add_project,name='add-project'),
    path('update-project/<str:project_id>',views.update_project,name='update-project'),
    path('delete-project',views.delete_project,name='delete-project'),

    path('like',views.like,name='like'),
    path('dislike',views.dislike,name='dislike'),
    
]