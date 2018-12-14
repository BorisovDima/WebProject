from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from project.apps.blog.shortcuts import render_to_html
import json


class EventConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group = 'user_event_%s' % self.scope['user'].id
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()



    async def get_event(self, event):
        notification = event['event']
        kwargs = event['kwargs']
        kwargs['data_publish'] = 'Now'
        kwargs['add'] = True
        html = await sync_to_async(render_to_html)('chat/message.html', kwargs)
        dialog = kwargs['id_dialog']
        await self.send(json.dumps({'event': notification, 'dialog': dialog, 'html': html}))
