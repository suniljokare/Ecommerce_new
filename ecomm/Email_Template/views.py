# from django.shortcuts import render
# from ecomm.settings import EMAIL_HOST_USER

# # Create your views here.
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string





# def send_mails(request):
#     if request.method == 'POST':
#             title = request.POST.get('title')
#             subject = request.POST.get('subject')
#             content = request.POST.get('content')
#             Template = request.POST.get('Template')
#             Msg = EmailMultiAlternatives(f'{subject}',f'{content}',EMAIL_HOST_USER,[f'{email}'])
#             Msg.attach_alternative(Template,"text/html")
#             Msg.send()
#             return render(request, 'myapp/Email_template.html')

#     else:
#         return render(request, 'myapp/Email_template.html')