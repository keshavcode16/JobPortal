from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from django.contrib.auth.models import AnonymousUser
from core_apps.authentication.models import User

from .tasks import notify_on_place_order
import json


class SavePostConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self,event):
        # self.threadId = self.scope['url_route']['kwargs']['threadId']
        # await self.channel_layer.group_add(
        #     self.threadId,
        #     self.channel_name
        # )
        await self.accept()
        await self.send(json.dumps({
            "type":"websocket.send",
            "text":"connected"
        }))
    
    async def websocket_receive(self, event):
        text_data_json = json.loads(event['text'])
        # action = text_data_json.get('action','')
        # threadId = text_data_json.get('threadId',None)
        # thread_payload = text_data_json.get('thread_payload',{})
        # if action == 'save_thread':
        #     profileId = text_data_json.get('profileId',None)
        #     channel_layer = get_channel_layer()
        #     save_post_thread_task.delay(thread_payload, profileId, threadId)
        await self.send(json.dumps({
            "type":"websocket.send",
            "text":"hello world"
        }))
   
    
    async def websocket_disconnect(self, event):
        print('disconnect', event)