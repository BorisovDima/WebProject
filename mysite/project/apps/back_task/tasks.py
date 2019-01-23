from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from  django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger()


@shared_task
def sendler_mail(subject, body, from_email, to_email, *, template_name=None, **kwargs):
    email_message = EmailMultiAlternatives(subject, body, from_email, to_email)
    if template_name:
        html_email = render_to_string(template_name, kwargs)
        email_message.attach_alternative(html_email, 'text/html')
    print(email_message.message())
    email_message.send()
    logging.info('Message send')



@shared_task
def delete_not_activ_user():
    model = get_user_model()
    delta = timezone.now() - timedelta(hours=12)
    users = model.objects.filter(is_verified=False).filter(date_joined__lt=delta)
    logging.info(users)
    users.delete()

