from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

import talk.routing
from talk import consumer
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack


# 主WS路由
# application = ProtocolTypeRouter({
#     'websocket': URLRouter([
#         path('talk/', consumer.ChatConsumer)
#     ])
# })



# application1 = ProtocolTypeRouter({
#     # 'websocket': AuthMiddlewareStack(          # 用于WebSocket认证，继承了Cookie Middleware，SessionMiddleware
#     'websocket': SessionMiddlewareStack(         # 使用Session中间件，可以请求中session的值
#         URLRouter(
#             talk.routing.websocket_urlpatterns
#         )
#     )
# })