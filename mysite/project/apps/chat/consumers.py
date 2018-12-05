from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from urllib.parse import parse_qs
from .models import Dialog, Message
import json
from django.utils import timezone
from project.apps.blog.shortcuts import render_to_html


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.dialog_id = self.scope['url_route']['kwargs']['id_dialog']
        self.group_d = 'dialog_%s' % self.dialog_id
        self.status = parse_qs(self.scope['query_string']).get(b'status')
        await self.channel_layer.group_add(self.group_d, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        if self.status == [b'New']:
            await database_sync_to_async(self.delete_new_close_dialog)()
        await self.channel_layer.group_discard(self.group_d,
                                               self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        kwargs = {'text': data['text'], 'dialog_id': self.dialog_id, 'author_id': self.scope['user'].id}
        self.status = b'Dont_new'
        to_user, msg_id = await database_sync_to_async(Message.objects.create_message)(**kwargs)
        kwargs['name_author'] = self.scope['user'].username
        kwargs['to_user'] = to_user.username
        kwargs['msg_id'] = msg_id
        await self.channel_layer.group_send(self.group_d,
                                            {'type': 'send_msg',
                                             'kwargs': kwargs})


    async def send_msg(self, event):
        kwargs = event['kwargs']
        if self.scope['user'].username == kwargs['to_user']:
            await database_sync_to_async(self.readed)(kwargs['msg_id'])
        kwargs['data_publish'] = 'Now '
        kwargs['dialog_read'] = True
        html = await sync_to_async(render_to_html)('chat/message.html', kwargs) # async def __call__
        await self.send(json.dumps({'message': html}))



    def delete_new_close_dialog(self):
        Dialog.objects.get(id=self.dialog_id).delete()

    def readed(self, msg_id):
        msg = Message.objects.get(id=msg_id)
        msg.user_readed_msg()







