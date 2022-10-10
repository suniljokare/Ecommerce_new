from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout,update_session_auth_hash
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm,PasswordChangeForm
from .helper import send_Foreget_Pass_mails






#signup view function

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm =SignupForm(request.POST)
            password = request.POST.get('password')

            if fm.is_valid():
                user =fm.save()
                user.set_password(password)
                user.save()
                messages.success(request,'your account has been signed up successfully!')
                return redirect('login')
        else:
            fm = SignupForm()
        return render(request, 'accounts/Registration.html',{'forms':fm})  

    else:
        return HttpResponseRedirect('/')


#login_page view function

def User_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request = request,data=request.POST)
            if fm.is_valid():
                umail = fm.cleaned_data.get('username')
                upass = fm.cleaned_data.get('password')
                user = authenticate(username=umail,password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request,"logged in successfully!")
                    return HttpResponseRedirect('/')
        else:      
            fm = AuthenticationForm()
        return render(request, 'accounts/login.html',{'forms':fm})
    else:
        return HttpResponseRedirect('/')



     









#Change password without old password for user profile function
# @login_required(login_url='accounts/login/') 
def Change_new_Password(request,token):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = SetPasswordForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request,'Password Change Successfully')
                # return HttpResponseRedirect('/')
        else:
            fm = SetPasswordForm(user=request.user)
        return render(request,'accounts/ChangePassword.html',{'forms':fm})
    else:
        return HttpResponseRedirect('/login/')
    





import uuid
#ForgetPassword View Function
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not CustomUserModel.objects.filter(email=username).first():
                messages.success(request,'Not User found with this username.')
                return redirect('/Forget_Password/')
            user_obj = CustomUserModel.objects.get(email=username)
            token = str(uuid.uuid4())
            send_Foreget_Pass_mails(user_obj,token)
            messages.success(request,' An Email is Sent.')
            return render(request, 'accounts/Reset_conf.html')
    except Exception as e:
         print(e)
    return render(request, 'accounts/ForgetPassword.html')





def reset_template(request):
    return render(request, 'accounts/Reset_conf.html')


# Change password with old password for user profile function

def ChangePassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request,'Password Change Successfully')
                return render(request, 'accounts/new_pass.html',{'forms':fm})
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/new_pass.html',{'forms':fm})
    else:
        return HttpResponseRedirect('/')



#logout View for user logout function

def User_logout(request):
    logout(request)
    return HttpResponseRedirect('/')





def UserProfiePage(request):
    if request.method == 'POST':
        fm =UserProfileForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Your UserProfile details has been  successfully completed!')
            # return HttpResponseRedirect('/')
            return render(request, 'accounts/User_Profile.html',{'forms':fm})
    else:
        fm = UserProfileForm()
    return render(request, 'accounts/User_Profile.html',{'forms':fm})  




def ContactUs(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm =ContactUsForm(request.POST)
            if fm.is_valid():
                user =fm.save()
                user.save()
                messages.success(request,'Thank You for Submitting Form!')
                return HttpResponseRedirect('/')
        else:
            fm = ContactUsForm()
        return render(request, 'accounts/ContactUs.html',{'forms':fm})
    else:
        return HttpResponseRedirect('/')