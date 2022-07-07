import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
# 源码 async_to_sync = AsyncToSync 即async_to_sync为类名，通过channel_layer.group_add, channel_layer.group_send, channel_layer.group_discard等初始化
# 初始化后的类实例可再被调用(调用到__call__方法)


# 同步：无法接受其他客户端的消息
class SyncChatConsumer(WebsocketConsumer):
    # 建立连接时触发
    def connect(self):
        self.accept()

    # 连接关闭时触发
    def disconnect(self, close_code):
        print('one client connect closed')
        pass

    # 在收到消息时触发
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = '我发送的消息：' + text_data_json['message']
        self.send(text_data=json.dumps({'message': message }))


# 引入channel layer
# !!! setting中配置通信后端
# python shell 测试
# import channels.layers
# channel_layer = channels.layers.get_channel_layer()
# async_to_sync(channel_layer.send)('test_channel', {'site': 'www.baidu.com'})
# async_to_sync(channel_layer.receive)('test_channel')               # 输出 www.baidu.com

class LayerSyncChatConsumer(WebsocketConsumer):                      # 依然同步
    def connect(self):
        print('--->:' + str(self.channel_layer))

        self.room_group_name = 'ops_coffee'
        self.channel_layer

        # Join room group
        async_to_sync(self.channel_layer.group_add)(                 # async_to_sync即AsyncToSync类， 先初始化AsyncToSync, 然后进行实例的调用(调用__call__)
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = '运维咖啡吧：' + event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


# 异步：实现多客户端聊天
class AsyncChatConsumer(AsyncWebsocketConsumer):                # 继承异步类 AsyncWebsocketConsumer
    async def connect(self):                                    # async异步函数定义
        self.room_group_name = 'ops_coffee'

        # Join room group
        await self.channel_layer.group_add(                     # await 来实现异步I/O的调用
            self.room_group_name,                               # 引入channel layer 也不在需要使用async_to_sync类了
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = '运维咖啡吧：' + event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))



