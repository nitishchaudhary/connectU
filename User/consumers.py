from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import DatabaseSyncToAsync

from Main.models import Message
User = get_user_model()
import asyncio
import json

class UserConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print('connected',event)
        user = self.scope['user']
        chat_room = f'user_chatroom_{user.username}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self,event):
        print('receive',event)
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        sent_by_username = received_data.get('sent_by')
        sent_to_username = received_data.get('sent_to')
        if not msg:
            return False
        sent_by_user = await self.get_user_object(sent_by_username)
        sent_to_user = await self.get_user_object(sent_to_username)
        other_user_chat_room = f"user_chatroom_{sent_to_username}"
        self_user = self.scope['user']
        response = {
            'message':msg,
            'sent_by':self_user.username
        }
        await self.channel_layer.group_send(
            other_user_chat_room,{
                'type':'chat_message',
                'text':json.dumps(response)
            }
        )
        await self.channel_layer.group_send(
            self.chat_room,{
                'type':'chat_message',
                'text':json.dumps(response)
            }
        )
        await self.save_message(sent_by_user,sent_to_user,msg)


    async def websocket_disconnect(self,event):
        print('disconnected',event)

    async def chat_message(self,event):
        await self.send({
            'type':'websocket.send',
            'text':event['text']
        })

    @DatabaseSyncToAsync
    def get_user_object(self,user_name):
        qs = User.objects.filter(username = user_name)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj
    
    @DatabaseSyncToAsync
    def save_message(self,sender_id,receiver_id,message):
        msg = Message.objects.create(sender_id = sender_id, reciever_id = receiver_id, message=message)
        msg.save()