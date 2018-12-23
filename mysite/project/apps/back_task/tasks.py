from celery import shared_task
from project.apps.blog.models import Article, Thread
from django.db.models import Count
from django.urls import reverse

import logging
logger = logging.getLogger()


@shared_task
def change_rating_post():
    change_rating(Article, 'views', '-id')

@shared_task
def change_rating_thread():
    change_rating(Thread, 'my_followers')


def change_rating(model, field, *args):
    print(field, *args)
    model.objects.filter(rating__gt=0).update(rating=0)
    for rating, post in enumerate(model.objects.annotate(count_=Count(field)).order_by(
                                                    *args,'-count_')[:250].iterator()):
        try:
            post.rating = rating+1
            post._save(update_fields=['rating'])
            logger.info(str(rating))
        except Exception:
            logger.error(str(post) + ' Error')
    logging.warning('Rating complet')

from django.core.mail import send_mail

@shared_task
def send_verify(uuid, email, name):
    send_mail('Verify your account %s ' % name,
              'Follow this link to verify your account: '
              '"http://localhost%s"' %  reverse('account:verify', kwargs={'uuid': uuid}), 'sup.raychan@mail.ru',
              [email],
              fail_silently=False)
