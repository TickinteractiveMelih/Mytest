import json
from channels.generic.websocket import WebsocketConsumer

from channels.generic.websocket import AsyncWebsocketConsumer


# class SceneChangeConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()  # WebSocket bağlantısını kabul edin

    

#     def receive(self, text_data):
#         # Gelen mesajı işle
#         data = json.loads(text_data)

#         self.send(text_data=json.dumps({
#             'message': 'change_scene',
#             'scene_name': data['scene_name']
#         }))
#         print(data)
        
#     def send_scene_change(self, event):
#         # WebSocket üzerinden gelen mesajı alın
#         message = event['message']

#         # Mesajı WebSocket istemcisine gönderin
#         self.send(text_data=json.dumps(message))


#     def disconnect(self, close_code):
#         pass  # Bağlantı kesildiğinde yapılacak işlemler

# class SceneChangeConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         data = json.loads(text_data)

#         # Gelen mesajı logla
#         print("Receivedd:", data)

#         # Belirli bir mesaj tipine göre yanıt gönder
#         if data.get('messageType') == 'trigger':
#             await self.send(text_data=json.dumps({
#                 'roomCode': data['roomCode'],
#                 'messageType': 'response',
#                 'content': 'Django: Mesaj alındı!'
#             }))

class SceneChangeConsumer(AsyncWebsocketConsumer):
    # def connect(self):
    #     self.accept()  # WebSocket bağlantısını kabul edin
    # def disconnect(self, close_code):
    #     pass
    # def receive(self, text_data):
    #     self.send(text_data='merhaba asd')
    async def connect(self):
        self.group_name = "unity_clients"  # Tüm Unity client'ların yer aldığı grup

        # Unity client'ı "unity_clients" grubuna ekleyin
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Unity client'ı gruptan çıkarın
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']

        # # Mesajı client'a geri gönderin (isteğe bağlı)
        # await self.send(text_data=json.dumps({
        #     'message': message
        # }))
        await self.send(text_data='merhaba asdff')
        
        message = {
        'mes': 'message1',
        'note': 'mtb',
    }
        await self.channel_layer.group_send(
            "unity_clients",
            {
                'type': 'send_user_properties',
                'message': message,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        # Mesajı WebSocket üzerinden client'a gönder
        await self.send(text_data=json.dumps({
            'message': message
        }))


class DeviceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_id = self.scope['url_route']['kwargs']['device_id']
        self.device_group_name = f"device_{self.device_id}"

        # Cihaz grubuna ekle
        await self.channel_layer.group_add(
            self.device_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Cihaz grubundan kaldır
        await self.channel_layer.group_discard(
            self.device_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        target_device_id = text_data_json.get('target_device_id')  # Hedef cihaz ID'si
        message = text_data_json.get('message')

        # Mesajı hedef cihaza gönder
        await self.channel_layer.group_send(
            f"device_{target_device_id}",
            {
                'type': 'device_message',
                'message': message
            }
        )

    async def device_message(self, event):
        message = event['message']

        # Mesajı WebSocket üzerinden gönder
        await self.send(text_data=json.dumps({
            'message': message
        }))