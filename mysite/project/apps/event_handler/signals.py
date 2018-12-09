from django.dispatch import receiver
from django import dispatch
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from project.apps.chat.models import Message
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from project.apps.back_task.tasks import send_verify

#my_message_signal = dispatch.Signal(providing_args=['instance', 'to_user', 'dialog_id'])


@receiver(post_save, sender=get_user_model(), dispatch_uid="my_user_handler")
def user_handler(sender, **kwargs):
    user = kwargs['instance']
    if not user.is_verified:
        uuid, email, name  = user.uuid, user.email, user.username
        send_verify.delay(uuid, email, name)


@receiver(post_save, sender=Message, dispatch_uid="my_message_handler")
def msg_handler(sender, **kwargs):
    if not kwargs['instance'].readed:
        user = kwargs['instance'].to_()
        group = 'user_event_%s' % user.id

        mykwargs = {}
        mykwargs['id_dialog'] = kwargs['instance'].dialog.id
        mykwargs['name_author'] = kwargs['instance'].author.username
        mykwargs['to'] = user.username
        mykwargs['text'] = kwargs['instance'].text

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(group,
                                                {'type': 'get_event',
                                                 'event': 'message',
                                                 'kwargs': mykwargs
                                                  })
                                             








