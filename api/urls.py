from django.urls import path
from .import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('',views.routes,name='routes'),
    path('projects/',views.projects,name='projectsapi'),
    path('projects/<str:pk>/',views.project,name='projectapi'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('projects/<str:pk>/vote/',views.projectVote,name='projectapivote'),
]
