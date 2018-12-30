from celery import shared_task
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from  django.utils import timezone
from datetime import timedelta

import logging
logger = logging.getLogger()



@shared_task
def send_verify(uuid, email, name):
    html_mail = render_to_string('back_task/mail_registr.html',
                                 {'link': 'http://localhost%s' %  reverse('myauth:verify',
                                                                            kwargs={'uuid': uuid})})
    text_mail = 'Follow this link to verify your account:'
    msg = EmailMultiAlternatives('Verify your account %s ' % name, text_mail, 'sup.raychan@mail.ru', [email])
    msg.attach_alternative(html_mail, "text/html")
    msg.send()

@shared_task
def sendler_mail(subject, body, from_email, to_email, html_email):
    print(from_email, to_email)
    email_message = EmailMultiAlternatives(subject, body, from_email, to_email)
    if html_email:
        print(html_email)
        email_message.attach_alternative(html_email, 'text/html')
    print(email_message)
    email_message.send()
    logging.info('Message send')



@shared_task
def delete_not_activ_user():
    model = get_user_model()
    delta = timezone.now() - timedelta(hours=12)
    users = model.objects.filter(is_verified=False).filter(date_joined__lt=delta)
    logging.info(users)
    users.delete()



#@shared_task
#def change_rating_post():
    #change_rating(Article, 'views', '-id')

#@shared_task
#def change_rating_community():
   # change_rating(Community, 'my_followers')


#def change_rating(model, field, *args):
 #   print(field, *args)
  #  model.objects.filter(rating__gt=0).update(rating=0)
  #  for rating, post in enumerate(model.objects.annotate(count_=Count(field)).order_by(
                                                  #  *args,'-count_')[:250].iterator()):
      #  try:
    #        post.rating = rating+1
      #      post._save(update_fields=['rating'])
     #       logger.info(str(rating))
      #  except Exception:
    #        logger.error(str(post) + ' Error')
 #   logging.warning('Rating complet')

