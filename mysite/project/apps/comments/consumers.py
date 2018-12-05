from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from project.apps.blog.models import Article
from .forms import CommentForm
from django.utils import timezone
from .models import Comment
from project.apps.blog.shortcuts import render_to_html
from django.contrib.auth import get_user_model

class CommentConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.article = self.scope['url_route']['kwargs']['slug']                  #name group
        await self.channel_layer.group_add(self.article, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.article,
                                               self.channel_name)

#########################################################
    async def receive(self, text_data):

        data = json.loads(text_data)
        #form = CommentForm(**data)

        #if not form.is_valid():
           # await self.send(json.dumps({'status': 'invalid'}))
        if not 1:
            pass
        else:
            article = await database_sync_to_async(self.get_article)(slug=self.article)
            kwargs = {'text': data['text'], 'author_id': self.scope['user'].id}
            mykwargs = kwargs.copy()

            if data['id_parent']:
                kwargs['parent_comment_id'] = data['id_parent']
                mykwargs['parent_name'] = data['name_parent']
                mykwargs['parent_id'] = data['id_parent']

            comment_id = await database_sync_to_async(Comment.objects.add_comment)(**kwargs, article=article)
            mykwargs['comment_id'] = comment_id
            mykwargs['author'] = self.scope['user'].username
            await self.channel_layer.group_send(self.article,
                                          {'type': 'send_comment',
                                              'kwargs': mykwargs})
    async def send_comment(self, event):
        kwargs = event['kwargs']
        kwargs.update({'create_data': timezone.now(), 'user': self.scope['user']})
        html = render_to_html('comments/comment.html', kwargs)
        await self.send(json.dumps({'comment': html}))

####################################################################
    def get_article(self, slug):
        return Article.objects.get(slug=slug)


