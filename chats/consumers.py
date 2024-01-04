import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime

from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        current_user_id=int(self.scope['query_string'])
        other_user_id=self.scope['url_route']['kwargs']['id']
        self.room_name=(
            f"{current_user_id}_{other_user_id}"
            if int(current_user_id) > int (other_user_id)
            else f"{other_user_id}_{current_user_id}"
        )

        self.room_group_name=f"chat_{self.room_name}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print("handshake connected websocket....")
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
        print("disconnect",self.channel_layer)
        await super().disconnect(close_code)

    
    async def receive(self, text_data=None, bytes_data=None):
        
        data=json.loads(text_data)
        message=data['message']
        sender_username=data['senderUsername']
        reciever_username = data['recieverUsername']
        sender=await self.get_user(sender_username)
        reciever=await self.get_user(reciever_username)

        await self.save_message(
            sender =sender,reciever=reciever,message=message,thread_name=self.room_group_name
        )

        messages=await self.get_messages()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":message,
                "senderUsername":sender_username,
                "messages":messages,
            }
        )

    async def chat_message(self,event):
        message=event["message"]
        username=event["senderUsername"]
        messages=event["messages"]


        await self.send(
            text_data=json.dumps(
                {
                    "message":message,
                    "senderUsername":username,
                    "messages":messages
                }
            )
        )

    @database_sync_to_async
    def get_user(self,username):

        return get_user_model().objects.filter(email=username).first()
    

    @database_sync_to_async
    def get_messages(self):
        from .serializers import MessageSerializer
        from .models import Message

        messages=[]
        for instance in Message.objects.filter(thread_name=self.room_group_name):
            messages=MessageSerializer(instance).data

        return messages
    

    @database_sync_to_async
    def save_message(self,sender,reciever,message,thread_name):

      
        from .models import Message
       
        Message.objects.create(
            sender=sender,reciever=reciever,message=message,thread_name=thread_name
        )
        
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from accounts.models import Notifications
        try:
            user_id = self.scope['url_route']['kwargs']['user_id']
            self.group_name = f'user_{user_id}'

            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            await self.accept()
        except Exception as e:
            print("error in connect :" ,e)

        

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        except Exception as e :
            print("error in disconnect",e)
    
    async def receive(self, text_data):
        try:
            message = json.loads(text_data)
            print("Recieved Message:",message)

            await self.save_notifications()
        except Exception as e:
            print("Error in recieve :",e)
    
    async def create_notification(self,event):

        try:
            message = event['message']

            await self.send(json.dumps({
                'type':'create_notification',
                'message':message
            }))

        except Exception as e:
            print("error in create notification",e)
    
    @database_sync_to_async
    def save_notifications(self,user,text):
        from accounts.models import Notifications
        Notifications.objects.create(
            user=user,text=text
        )
    



class AdminNotifications(AsyncWebsocketConsumer):
    async def connect(self):
        from accounts.models import Notifications
        try:
            self.group_name = 'admin_group'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            print('connected ')
            await self.accept()
        except Exception as e:
            print("Error in connect in admin noti", e)
    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        except Exception as e:
            print("Error in disconnect admin notif:", e)


    async def receive(self, text_data):
        try:
            message = json.loads(text_data)
            print("admin_Received message:", message)
        except Exception as e:
            print("Error in receive admin noti:", e)


    async def create_notification(self, event):
        try:
            message = event['message']
            await self.send(json.dumps({
             
                'message': message
            }))
        except Exception as e:
            print("Error in create admin notif:", e)
