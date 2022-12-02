# import os
# from sendgrid import SendGridAPIClient,Mail
# from django.conf import settings    
# from sendgrid.helpers.mail import Mail

# message = Mail(
#     from_email='sunil.jokare@gmail.com',
#     to_emails='sunil.jokare@gmail.com',
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>')

# sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
# response = sg.send(message)
# print(response.status_code, response.body, response.headers)

# from django.conf import settings    
# import sendgrid
# import os
# from sendgrid.helpers.mail import Attachment, ContentId, Disposition, FileContent, FileName, FileType, Mail

# sg = sendgrid.SendGridAPIClient((settings.SENDGRID_API_KEY))
# data = {
#   "personalizations": [
#     {
#       "to": [
#         {
#           "email": "sunil.jokare@gmail.com"
#         }
#       ],
#       "subject": "Sending with SendGrid is Fun"
#     }
#   ],
#   "from": {
#     "email": "sunil.jokare@gmail.com"
#   },
#   "content": [
#     {
#       "type": "text/plain",
#       "value": "and easy to do anywhere, even with Python"
#     }
#   ]
# }
# response = sg.client.mail.send.post(request_body=data)
# print(response.status_code)
# print(response.body)
# print(response.headers)


from django.core.mail import send_mail
from django.conf import settings

send_mail('Testing mail', 'A cool message :)', 'sunil.jokare@gmail.com', ['sunil.jokare@gmail.com'])
