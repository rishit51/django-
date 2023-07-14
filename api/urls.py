from django.urls import path
from .import views
urlpatterns = [
    path('',views.routes,name='routes'),
    path('projects/',views.projects,name='projectsapi'),
    path('projects/<str:pk>/',views.project,name='projectapi')
]
