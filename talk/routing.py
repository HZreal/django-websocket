from django.urls import path
from talk import consumer

websocket_urlpatterns = [
    # path('ws/talk/', consumer.SyncChatConsumer.as_asgi()),           # 同步
    # path('ws/talk/', consumer.LayerSyncChatConsumer.as_asgi()),      # 引入channel layer的同步
    path('ws/talk/', consumer.AsyncChatConsumer.as_asgi()),            # 异步
]