from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('login_1/',LoginView.as_view(),name='login'),
    path('register/',SignUpView.as_view(),name='register'),
    path('change_password/<email_token>/',ResetPasswordView.as_view(),name='change_password'),
    path('new_password/',login_required(ChangePasswordView.as_view()),name='new_password'),
    path('Forget_Password/',ForgetPasswordView.as_view(),name='Forget_Password'),
    path('user_logout/',login_required(LogoutView.as_view()), name='user_logout'),
    path('contactus/',ContactUsView.as_view(), name='contactus'),
    path('userprofilepage/',UserProfilView.as_view(), name='userprofilepage'),
    path("addresses/edit/<slug:pk>/", edit_address.as_view(), name="edit_address"),
    path("addresses/delete/<slug:pk>/",delete_address.as_view(), name="delete_address"),
    path("addresses/set_default/<slug:pk>/",SetDefaultView.as_view(), name="set_default"),
    path('adresses/',AddressView.as_view(), name='adresses'),
    path('singleblog/',singleblog, name='singleblog'),
    path('bloglist/',bloglist, name='bloglist'),
    path('shop/',shop, name='shop'),
    path('reset/',reset_template,name='reset'),
    path('activate_email/<email_token>/', activate_email, name="activate_email"),


]


