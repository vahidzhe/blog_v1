from django.urls import path
from . views import *
urlpatterns = [
    path('register',user_register,name = 'register'),
    path('login',user_login,name = 'login'),
    path('logout',user_logout,name = 'logout'),
    path('profile_edit',profile_edit,name = 'profile_edit'),
    path('password_edit',password_edit,name = 'password_edit'),
    
    path('profile_photo_edit',profile_photo_edit,name = 'profile_photo_edit'),
    path('user_visible',user_visible,name = 'user_visible'),
    path('<username>/user_followers',user_followers,name = 'user_followers'),
    path('<username>/user_followeds',user_followeds,name = 'user_followeds'),
    path('<username>',dashboard,name = 'dashboard'),
    
    

]