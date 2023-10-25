import json
from random import randint
from time import sleep

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ConversationConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None

    async def connect(self):
        print("connecté au websocket")
        await self.accept()
        await self.send_json({
            "type": "chat_message",
            "message": "salut",
        })

    def disconnect(self, code):
        print("Disconnected!")
        return super().disconnect(code)

    def receive_json(self, content, **kwargs):
        print(content)
        return super().receive_json(content, **kwargs)
