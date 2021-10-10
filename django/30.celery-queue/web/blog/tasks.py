from django.core.mail import send_mail
from time import sleep
from celery import shared_task

@shared_task
def send_email(subject, message):
    sleep(10)
    mail = {
        'subject': subject,
        'message': message,
        'from_email': 'admin@example.com',
        'recipient_list': [
            'user@example.com',
            ]
        }
    send_mail(**mail)
