import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PaymentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Lấy orderId từ URL
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f"payment_{self.order_id}"
        
        # Tham gia vào nhóm để nhận thông báo về trạng thái thanh toán
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Rời khỏi nhóm khi kết nối bị đóng
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Nhận thông báo từ nhóm và gửi lại cho WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    # Nhận thông báo về trạng thái thanh toán từ backend (bạn sẽ gửi thông báo vào đây)
    async def payment_status_update(self, event):
        # Gửi thông tin thanh toán vào WebSocket
        await self.send(text_data=json.dumps({
            'status': event['status'],
            'message': event['message']
        }))