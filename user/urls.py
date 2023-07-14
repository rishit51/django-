from django.urls import path
from .import views
urlpatterns = [
    path('',views.profiles,name='profiles'),
    path('user-profile/<str:uid>',views.profile,name='profile'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logOut,name='logout'),
    path('register/',views.register,name='register'),
    path('account/',views.userAccount,name="account"),
    path('edit-account/',views.editAccount,name='edit-account'),
    path('create-skill/',views.createSkill,name='createskill'),
    path('update-skill/<str:pk>',views.updateSkill,name='updateskill'),path('delete-skill/<str:pk>',views.deleteSkill,name='deleteskill'),
    path('message/<str:id>',views.message,name='message'),
    path('inbox/',views.inbox,name='inbox'),
    path('send-message/<str:pk>',views.createMessage,name='createmess')

]
