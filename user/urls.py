from django.urls import path
from .import views
urlpatterns = [
    path('',views.profiles,name='profiles'),
    path('user-profile/<str:uid>',views.profile,name='profile'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logOut,name='logout'),
    path('register/',views.register,name='register'),
    path('account/',views.userAccount,name="account")

]
