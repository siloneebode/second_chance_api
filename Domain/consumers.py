from channels.generic.websocket import AsyncJsonWebsocketConsumer

from Domain.services import get_user_channels


class UserConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        user = self.scope['user']
        if user.is_authenticated:
            # Si le user est authentifié on l'ajoute dans tous ses groups de canaux
            channels = get_user_channels(user)
            for channel in channels:
                await self.channel_layer.group_add(
                    channel,
                    self.channel_name
                )

    async def disconnect(self, close_code):
        user = self.scope['user']
        if user.is_authenticated:
            # Remove user from all public channels groups they are subscribed to
            channels = get_user_channels(user)
            for channel in channels:
                await self.channel_layer.group_discard(
                    channel.name,
                    self.channel_name
                )

    async def notification_message(self, event):
        pass
        # Send notification message to client
        #message = event['message']
        #await self.send(text_data=json.dumps({
        #    'message': message
        #}))

    def receive_json(self, content, **kwargs):
        print(content)
        return super().receive_json(content, **kwargs)
