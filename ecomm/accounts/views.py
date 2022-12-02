from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from .models import *
from .forms import *
from django.contrib import messages as mymessage
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm,PasswordChangeForm
from base.helper import send_emails
import uuid
from django.views import View
from django.contrib.auth.decorators import login_required
import json
from django.urls import reverse_lazy    
from django.views.generic.edit import UpdateView,CreateView ,DeleteView  
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, RedirectView



##################################### User management #####################################

# SINGUP
class SignUpView(CreateView):  
    model = CustomUserModel  
    fields=('first_name','last_name','email','password')
    success_url = '/accounts/login_1/' 

    def form_valid(self, form,commit=True):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        if commit:
            user.save()
        messages.success(self.request,'your account has been signed up successfully!')
        return super().form_valid(form)


#LOGIN 
class LoginView(View):
    return_url = None

    def get(self, request,*args):
        LoginView.return_url = request.GET.get('return_url')
        form = AuthenticationForm()
        return render(self.request, 'accounts/login.html',{'form':form })

    def post(self,request,*args):
        fm = AuthenticationForm(request = self.request,data=self.request.POST)
        if fm.is_valid():
            umail = fm.cleaned_data.get('username')
            user = CustomUserModel.object.get(email=umail)
            upass = fm.cleaned_data.get('password')

            if not user.is_email_verified:
                messages.warning(request, 'Your account is not verified.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = authenticate(username=umail,password=upass)
        
            if user is not None or user.is_superuser==True:
                login(self.request, user)
                messages.success(request,f'welcome  {user.first_name} !!!!!!')
                request.session['customer'] = user.id

                if LoginView.return_url:
                    return HttpResponseRedirect(LoginView.return_url)
             
                else:
                    LoginView.return_url = None
                    return redirect('homepage')

            messages.success(request, 'user is not registered ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:      
            messages.success(self.request,'wrong ')
        return render(self.request, 'accounts/login.html',{'form':fm, 'errors': fm.errors})



# EMAIL VERIFICATION
def activate_email(request, email_token):

    try:
        user = CustomUserModel.objects.get(token_no= email_token)
        user.is_email_verified = True   
        user.save()
        return redirect('login')
    except Exception as e:
        return HttpResponse('Invalid Email token')


# RESET PASSWORD
# @login_required(login_url='accounts/login/') 
class ResetPasswordView(View):

    def get(self,request,email_token):
        fm = SetPasswordForm(user=request.user)
        return render(request,'accounts/changepassword.html',{'form':fm})

    def post(self,request,email_token):
        fm = SetPasswordForm(user=request.user,data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            messages.success(request,'Password Change Successfully')
            return HttpResponseRedirect('/accounts/login_1/')

        return HttpResponseRedirect('/login/')


#FORGET PASSWORD 
class ForgetPasswordView(View):

    def get(self,request):
        return render(request, 'accounts/forgetpassword.html')  

    def post(self,request):
        username = request.POST.get('username')

        if not CustomUserModel.objects.filter(email=username).first():
            messages.success(request,'Not User found with this username.')
            return redirect('/Forget_Password/')
        user_obj = CustomUserModel.objects.get(email=username)
        email_token = str(uuid.uuid4())
        messages = f'Hi, click on this link to reset your password http://127.0.0.1:8000/accounts/change_password/{email_token}/'

        send_emails(user_obj,messages)

        # messages.success(request,' An Email is Sent.')
        return render(request, 'accounts/resetconfg.html')


# CHANGE PASSWORD
class ChangePasswordView(View):

    def get(self,request):
        fm = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/newpassword.html',{'form':fm})
    
    def post(self,request):
        fm = PasswordChangeForm(user=request.user,data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            messages.success(request,'Password Change Successfully')
            return render(request, 'accounts/newpassword.html',{'form':fm})
        
        return render(request, 'accounts/newpassword.html',{'form':fm})
        

#LOGOUT
class LogoutView(RedirectView):
    url = '/'
    def get(self, request):
        logout(request)
        return super(LogoutView, self).get(request)


############################# User Profile Management  ############################################


class UserProfilView(CreateView):  
    model = UserProfile  
    form_class = UserProfileForm
    success_url = '/' 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddressView(ListView):
    template_name = 'accounts/userprofile_list.html'
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class edit_address(UpdateView):  
    model = UserProfile  
    form_class = UserProfileForm
    success_url = '/' 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class delete_address(DeleteView):
    model = UserProfile  
    success_url = '/'  


class SetDefaultView(RedirectView):
    url = '/accounts/adresses'
    def get(self, request,pk):
        UserProfile.objects.filter(user=request.user, default=True).update(default=False)
        UserProfile.objects.filter(pk=pk, user=request.user).update(default=True)
        return super(SetDefaultView, self).get(request)


class ContactUsView(FormView):
    form_class = ContactUsForm
    template_name = 'accounts/contactus.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()   
        # self.send_mail(form.cleaned_data)
        return super(ContactUsView, self).form_valid(form)


####################################### BLOG ###################################

def singleblog(request):
    return render(request, 'accounts/singleblog.html' )

def bloglist(request):
    return render(request, 'accounts/bloglist.html' )

def shop(request):
    return render(request, 'accounts/shop.html' )

def reset_template(request):
    return render(request, 'accounts/Reset_conf.html')
















# def User_login(request):
#     if not request.user.is_authenticated:
#         if request.method == 'POST':
#             fm = AuthenticationForm(request = request,data=request.POST)

#             if fm.is_valid():
#                 umail = fm.cleaned_data.get('username')
#                 upass = fm.cleaned_data.get('password')

#                 # if not umail.is_email_verified:
#                 #     messages.warning(request, 'Your account is not verified.')
#                 #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#                 user = authenticate(username=umail,password=upass)
#                 if user is not None:
#                     dj_login(request, user)
#                     mymessage.success(request,f'welcome  {user.first_name} !!!!!!')
#                     return HttpResponseRedirect('/')
#         else:      
#             fm = AuthenticationForm()
#         return render(request, 'accounts/login.html',{'forms':fm})
#     else:
#         return HttpResponseRedirect('/')




# def Change_new_Password(request,token):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             fm = SetPasswordForm(user=request.user,data=request.POST)
#             if fm.is_valid():
#                 fm.save()
#                 update_session_auth_hash(request, fm.user)
#                 messages.success(request,'Password Change Successfully')
#                 # return HttpResponseRedirect('/')
#         else:
#             fm = SetPasswordForm(user=request.user)
#         return render(request,'accounts/ChangePassword.html',{'forms':fm})
#     else:
#         return HttpResponseRedirect('/login/')



# def ForgetPassword(request):
#     try:
#         if request.method == 'POST':
#             username = request.POST.get('username')

#             if not CustomUserModel.objects.filter(email=username).first():
#                 messages.success(request,'Not User found with this username.')
#                 return redirect('/Forget_Password/')
#             user_obj = CustomUserModel.objects.get(email=username)
#             email_token = str(uuid.uuid4())
#             messages = f'Hi, click on this link to reset your password http://127.0.0.1:8000/accounts/change_password/{email_token}/'

#             send_account_activation_email(user_obj,messages)
#             messages.success(request,' An Email is Sent.')
#             return render(request, 'accounts/Reset_conf.html')
#     except Exception as e:
#          print(e)
#     return render(request, 'accounts/ForgetPassword.html')



# def ChangePassword(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             fm = PasswordChangeForm(user=request.user,data=request.POST)
#             if fm.is_valid():
#                 fm.save()
#                 update_session_auth_hash(request, fm.user)
#                 messages.success(request,'Password Change Successfully')
#                 return render(request, 'accounts/new_pass.html',{'forms':fm})
#         else:
#             fm = PasswordChangeForm(user=request.user)
#         return render(request, 'accounts/new_pass.html',{'forms':fm})
#     else:
#         return HttpResponseRedirect('/')



# def reset_template(request):
#     return render(request, 'accounts/Reset_conf.html')


# def User_logout(request):
#     logout(request)
