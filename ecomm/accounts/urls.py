from django.urls import path
from .views import *

urlpatterns = [
    path('login/',User_login,name='login'),
    path('register/',signup,name='register'),
    path('change_password/<token>/',Change_new_Password,name='change_password'),
    path('new_password/',ChangePassword,name='new_password'),
    path('Forget_Password/',ForgetPassword,name='Forget_Password'),
    path('reset/',reset_template,name='reset'),
    path('user_logout/',User_logout, name='user_logout'),
    path('profile/',UserProfiePage, name='profie'),
    path('contactus/',ContactUs, name='contactus'),
] 