from django import forms
from .models import *



class SignupForm(forms.ModelForm):
    class Meta:
        model= CustomUserModel
        fields=('first_name','last_name','email','password')
        
        labels ={'first_name':'','last_name':'','email':'','password':''}
        
        error_messages = {
            'first_name':{'required':'Please enter a first_name'},
            'last_name':{'required':'Please enter a last_name'},
            'email':{'required':'Please enter a email address'},
            'password':{'required':'Please enter a valid password'}, }
            
        widgets = {
                'password':forms.PasswordInput(attrs={'class':'myclass','placeholder':'Password'}),
                'first_name':forms.TextInput(attrs={'class':'myclass','placeholder':'First_name '}),
                'last_name':forms.TextInput(attrs={'class':'myclass','placeholder':'Last_name '}),
                'email':forms.TextInput(attrs={'class':'myclass','placeholder':'Email Address '}),}




class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile

        fields=('image','country','state','city','address_1','address_2','zipcode')

        labels = {'image':'User Profile Image',}

        error_messages = {
            'image':{'required':'Please upload a user profile image'},
            'country':{'required':'Please select a country'},
            'state':{'required':'Please select a state'},
            'city':{'required':'Please select a city'},
            'address_1':{'required':'Please select a address_1'},
            'address_2':{'required':'Please select a address_2'},
            'zipcode':{'required':'Please select a zipcode'},
        }

        widgets = {
            'country':forms.TextInput(attrs={'class':'myclass','placeholder':'Please Enter  country'}),
            'city':forms.TextInput(attrs={'class':'myclass','placeholder':'Please Enter  city'}),
            'address_1':forms.TextInput(attrs={'class':'myclass','placeholder':'Please Enter  address_1'}),
            'address_2':forms.TextInput(attrs={'class':'myclass','placeholder':'Please Enter  address_2'}),
            'zipcode':forms.TextInput(attrs={'class':'myclass','placeholder':'Please Enter  zipcode'}),
        }



class ContactUsForm(forms.ModelForm):
    
    class Meta:
        model = ContactUs
        
        fields=('name','email','contact_no','subject','message')

        labels = {'name':'Full Name :','email':'Email Address:','contact_no':'Contact Number','subject':'Subject :','message':'Message :'}

        error_messages = {
            'name':{'required':'Please Enter a Full Name'},
            'email':{'required':'Email Address Required'},
            'contact_no':{'required':'Mobile Number Required'},
            'city':{'required':'Please Enter a City'},
            'subject':{'required':'Please Enter a Subject'},
            'message':{'required':'Please Enter a Message'},
        }

        widgets = {
            'name':forms.TextInput(attrs={'class':'myclass','placeholder':'Full Name'}),
            'email':forms.TextInput(attrs={'class':'myclass','placeholder':'Email Address'}),
            'contact_no':forms.TextInput(attrs={'class':'myclass','placeholder':'Mobile Number'}),
            'city':forms.TextInput(attrs={'class':'myclass','placeholder':'City'}),
            'subject':forms.TextInput(attrs={'class':'myclass','placeholder':'Subject'}),
            'message':forms.TextInput(attrs={'class':'myclass','placeholder':'Message'}),

        }
