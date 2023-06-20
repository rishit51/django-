from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('projects/<str:pk>',views.project,name='single-project'),
    path('create-project',views.createProject,name='create-proj'),
    path('updateProj/<str:pk>',views.updateProject,name='update-pro'),
    path('delete<str:pk>',views.delProject,name='del_proj')

]
