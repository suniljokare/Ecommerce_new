from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import Usermanager
from django.db.models.signals import post_save
from django.dispatch import receiver
from base.helper import send_emails
import uuid
from django.utils.translation import gettext_lazy as _
from base.constant import *

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now= True)
    created_by = models.CharField(max_length=255, default='dj')
    updated_at = models.DateTimeField(auto_now_add= True)
    updated_by = models.CharField(max_length=255, default='dj')


    class Meta:
        abstract = True




class CustomUserModel(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    token_no = models.CharField(max_length=255 )
    status = models.BooleanField(default=False)
    fb_token = models.CharField(max_length=100)
    twitter_token =  models.CharField(max_length=100)
    google_token = models.CharField(max_length=100)
    registration_method =  models.CharField(max_length=1,  choices = CHOICES, default='N')

    object = Usermanager()

    def __str__(self):
        return self.email
    


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
   




class UserProfile(BaseModel):
    user = models.ForeignKey(CustomUserModel , on_delete=models.CASCADE , related_name="CustomUserModel")
    image = models.ImageField(default="",upload_to='profile_pics')
    mobile_number = models.CharField(max_length=12,null=True, blank=True )
    address_1 = models.CharField(max_length=200)
    address_2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(choices=STATE_CHOICES,max_length=50)
    country = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    # status = models.BooleanField('_("Default")', default=False)
    default = models.BooleanField(_("Default"), default=False)

    # def __str__(self):
    #     return (self.user.first_name)



# Contact Us ModelForm
class ContactUs(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=12)
    message = models.TextField()
    note_admin = models.TextField(max_length=100 , blank=True, null=True)


    def __str__(self):
        return self.name
    
