from django.db.models.signals import post_save
from django.dispatch import receiver
from base.helper import send_emails
import uuid
from products.models import *



@receiver(post_save,sender = CustomUserModel)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email = instance.email
            email_token = str(uuid.uuid4())
            instance.token_no = email_token
            instance.save()
            messages = f'Hi, click on this link to verify your account http://127.0.0.1:8000/accounts/activate_email/{email_token}/'
            send_emails(email, messages)

    except Exception as e:
        print(e)
