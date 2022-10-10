from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import Usermanager



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now= True)
    created_by = models.CharField(max_length=255, default='dj')
    updated_at = models.DateTimeField(auto_now_add= True)
    updated_by = models.CharField(max_length=255, default='dj')


    class Meta:
        abstract = True


CHOICES =(
    ("N", "Normal"),
    ("F", "Fcaebook"),
    ("G", "Google"),
    ("T", "Twitter"),
)   
class CustomUserModel(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False,null=True,)
    email_token = models.CharField(max_length=100 , null=True , blank=True)
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
   




   
STATE_CHOICES = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),
("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),
("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),
("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),
("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),
("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),
("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),
("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),
("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),
("Puducherry","Puducherry"))



class UserProfile(BaseModel):
    user = models.ForeignKey(CustomUserModel , on_delete=models.CASCADE , related_name="CustomUserModel")
    image = models.ImageField(default="",upload_to='profile_pics')
    address_1 = models.CharField(max_length=200)
    address_2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(choices=STATE_CHOICES,max_length=50)
    country = models.CharField(max_length=100)
    zipcode = models.IntegerField()

    def __str__(self):
        return self.user
    



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
    