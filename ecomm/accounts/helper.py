from django.shortcuts import render
from ecomm.settings import EMAIL_HOST_USER


# Create your views here.
from django.core.mail import EmailMultiAlternatives
import uuid




def send_Foreget_Pass_mails(email,token):
   
    subject = 'Your foreget password link '
    messages = f'Hi, click on this link to reset your password http://127.0.0.1:8000/accounts/change_password/{token}/'
    email_from = EMAIL_HOST_USER
    recipient_list = [email]
    Msg = EmailMultiAlternatives(subject,messages,email_from,recipient_list)
    Msg.send()
    return True 

