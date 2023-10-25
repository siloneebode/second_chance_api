from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None

    async def connect(self):
        print("Websocket connected...")

    async def receive(self):
        print('Message received')

    async def disconnect(self, code):
        print('buy')
