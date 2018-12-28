from django.dispatch import receiver
from django import dispatch
from django.db.models.signals import post_save, pre_delete, post_delete
from asgiref.sync import async_to_sync
from project.apps.chat.models import Message
from project.apps.like_dislike.models import Like, Subscribe
from project.apps.comments.models import Comment
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from project.apps.back_task.tasks import send_verify
from project.apps.blog.models import Article, Community

#my_message_signal = dispatch.Signal(providing_args=['instance', 'to_user', 'dialog_id'])


@receiver(post_save, sender=get_user_model(), dispatch_uid="my_user_handler")
def user_handler(sender, **kwargs):
    user = kwargs['instance']
    if not user.is_verified and user.email:
        uuid, email, name = user.uuid, user.email, user.username
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

from .models import Notification


def notify(id, owner, initiator, content_object, event):
    Notification.objects.create(owner=owner,
                                initiator=initiator,
                                content_object=content_object, event=event)
    group = 'user_event_%s' % id
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group,
                                            {'type': 'get_event',
                                             'event': 'notify',
                                             })


@receiver(post_save, sender=Like, dispatch_uid="my_like_handler")
def like_handler(sender, **kwargs):
    user = kwargs['instance'].content_object.author
    if user == kwargs['instance'].user:
        return
    notify(user.id, user, kwargs['instance'].user, kwargs['instance'], 'L')


@receiver(post_save, sender=Subscribe, dispatch_uid="my_subs_handler")
def subs_handler(sender, **kwargs):
    if kwargs['instance'].content_object.__class__ != Community:
        user = kwargs['instance'].content_object
        notify(user.id, user, kwargs['instance'].user, kwargs['instance'], 'S')


@receiver(post_save, sender=Comment, dispatch_uid="my_comment_handler")
def comment_handler(sender, **kwargs):
    if kwargs['instance'].article.author == kwargs['instance'].author:
        return
    if kwargs['instance'].parent_comment:
        user = kwargs['instance'].parent_comment.author
        notify(user.id, user, kwargs['instance'].author, kwargs['instance'], 'C')
        if kwargs['instance'].parent_comment.author == kwargs['instance'].article.author:
            return
    user = kwargs['instance'].article.author
    notify(user.id, user, kwargs['instance'].author, kwargs['instance'], 'CP')




from django.contrib.contenttypes.models import ContentType

def del_event(kwargs):
    event, id = ContentType.objects.get_for_model(kwargs['instance']), kwargs['instance'].id
    print(Notification.objects.filter(content_type=event, object_id=id).delete())


@receiver(post_delete, sender=Like, dispatch_uid="my_like_del")
def like_delete_notify(sender, **kwargs): del_event(kwargs)

@receiver(pre_delete, sender=Comment, dispatch_uid="my_comment_del")
def commment_delete_notify(sender, **kwargs): del_event(kwargs)

@receiver(pre_delete, sender=Subscribe, dispatch_uid="my_subs_del")
def subs_delete_notify(sender, **kwargs): del_event(kwargs)


