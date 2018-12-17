from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from project.apps.blog.models import Article
from .forms import CommentForm
from django.utils import timezone
from .models import Comment
from project.apps.blog.shortcuts import render_to_html
from asgiref.sync import sync_to_async

class CommentConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.id_article = self.scope['url_route']['kwargs']['id']                  #name group
        self.group = 'post_%s' % self.id_article
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group,
                                               self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        form = CommentForm(data)
        if not form.is_valid():
           await self.send(json.dumps({'status': 'invalid'}))
        else:
            kwargs = {'text': data['text'], 'author_id': self.scope['user'].id, 'article_id': self.id_article}
            mykwargs = kwargs.copy()
            if data['id_parent']:
                kwargs['parent_comment_id'] = data['id_parent']
                mykwargs['parent_name'] = data['name_parent']
                mykwargs['parent_id'] = data['id_parent']

            comment_id = await database_sync_to_async(Comment.objects.add_comment)(**kwargs)
            mykwargs['comment_id'] = comment_id
            mykwargs['author'] = self.scope['user'].username
            await self.channel_layer.group_send(self.group,
                                          {'type': 'send_comment',
                                              'kwargs': mykwargs})
    async def send_comment(self, event):
        kwargs = event['kwargs']
        kwargs.update({'create_data': timezone.now(), 'user': self.scope['user']})
        html = await sync_to_async(render_to_html)('comments/comment.html', kwargs)
        await self.send(json.dumps({'comment': html, 'status': 'ok'}))


    async def delete_post(self, event):
        await self.send(json.dumps({'status': 'del_post'}))
