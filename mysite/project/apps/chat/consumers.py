from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from urllib.parse import parse_qs
from .models import Dialog, Message
import json
from django.template.loader import render_to_string
from .forms import DialogForm

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
        form = DialogForm(data)
        if not form.is_valid():
            await self.send(json.dumps({'status': 'invalid'}))
        else:
            kwargs = {'text': data['text'], 'dialog_id': self.dialog_id, 'author_id': self.scope['user'].id}
            self.status = b'Dont_new'
            msg_id = await database_sync_to_async(Message.objects.create_message)(**kwargs)
            await self.channel_layer.group_send(self.group_d,
                                                {'type': 'send_msg',
                                                'id': msg_id})


    async def send_msg(self, event):
        msg = await database_sync_to_async(self.get_msg)(event['id'])
        to_ = msg.to_()
        if self.scope['user'].username == to_:
            msg.user_readed_msg()
        html = await sync_to_async(render_to_string)('chat/message.html', {'name_author': msg.author, 'to': to_,
                                                                           'data_publish': 'now', 'text': msg.text})
        await self.send(json.dumps({'message': html, 'status': 'ok'}))



    def delete_new_close_dialog(self):
        Dialog.objects.get(id=self.dialog_id).delete()

    def get_msg(self, msg_id):
        return Message.objects.get(id=msg_id)






