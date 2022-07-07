import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import datetime

# 前端创建websocket对象后可以通过onmessage监听并处理后端返回的数据，可以通过send方法向后端发送数据
# 每个频道(channel)都有一个名字，拥有频道名称的任何人都可以向频道发送消息。一个组(group)有一个名字，可以包含多个频道

# WebsocketConsumer类为同步的
# AysncWebSocketConsumer类为异步的
# 每个自定义的Consumer类自带了 self.channel_name 和 self.channel_layer属性
# 前者是独一无二的长连接频道名，后者提供了 send(), group_send()和group_add() 3种方法, 可以给单个频道或一个频道组发信息，还可以将一个频道加入到组

# 注意：异步Consumer类性能更优，channels推荐使用同步consumer类 , 尤其是调用Django ORM或其他同步程序时，以保持整个consumer在单个线程中并避免ORM查询阻塞整个event。调用channel_layer提供的方法时需要用async_to_sync转换一下

# scope对象类似于Django的request对象，它代表了当前websocket连接的所有信息，比如scope['user'], scope['path']
# self.scope['url_route']['kwargs']['room_name']从路由中获取了聊天室的房间名，在channels程序中，scope是个很重要的对象，类似于django的request对象，它代表了当前websocket连接的所有信息。你可以通过scope['user']获取当前用户对象，还可以通过scope['path']获取当前当前请求路径

class ChatConsumer(WebsocketConsumer):
    # websocket建立连接时执行方法
    def connect(self):
        # 从url里获取聊天室名字，为每个房间建立一个频道组
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # 将当前频道加入频道组
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # 接受所有websocket请求
        self.accept()

    # websocket断开时执行方法
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # 从websocket接收到消息时执行函数
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 发送消息到频道组，频道组调用chat_message方法
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # 从频道组接收到消息后执行方法
    def chat_message(self, event):
        message = event['message']
        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 通过websocket发送消息到客户端
        self.send(text_data=json.dumps({
            'message': f'{datetime_str}:{message}'
        }))