from django.dispatch import receiver
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from .models import Message
from channels.layers import get_channel_layer
import json








@receiver(post_save, sender=Message, dispatch_uid="my_message_handler")
def handler_message(sender, **kwargs):
    user = kwargs['instance'].to_()
    group = 'user_event_%s' % user.id
    print(group)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group,
                                            {'type': 'get_event',
                                            'event': 'message'})




