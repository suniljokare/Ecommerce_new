from io import BytesIO
from itertools import product
from re import template
import uuid
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa 
from django.conf import settings
from django.shortcuts import render
from ecomm.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
import uuid
from django.template.loader import render_to_string



def save_pdf(params:dict):
    template = get_template("products/invoice.html")
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name =str(uuid.uuid4())

    try:
        with open(str(settings.BASE_DIR)+F"/public/{file_name}.pdf", "wb+") as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
        
    except Exception as e:
        print(e)
            
    
    if pdf.err:
        return '' , False
    
    return file_name, True



def send_emails(email,messages,*args):

    subject = 'Your foreget password link '
    recipient_list = [email]
    email_from = EMAIL_HOST_USER
    Msg = EmailMultiAlternatives(subject,messages,email_from,recipient_list)
    Msg.send()
    return True 


def order_placed_mail(order):
    html_body = render_to_string("products/order_placed.html", {'order':order})
    message = EmailMultiAlternatives(
        subject='Django HTML Email',
        body="mail testing",
        from_email=settings.FROM_EMAIL,
        to=[order.email]
        )
    message.attach_alternative(html_body, "text/html")
    message.send(fail_silently=False)
    

def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None



