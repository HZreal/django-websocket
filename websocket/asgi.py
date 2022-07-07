"""
ASGI config for websocket project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing, talk.routing, kuayu.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websocket.settings')


# application = get_asgi_application()          # 仅http请求支持


# channels的ProtocolTypeRouter会根据请求协议的类型来转发请求
application = ProtocolTypeRouter({
    # HTTP请求处理
    "http": get_asgi_application(),

    # websocket请求处理
    "websocket": AuthMiddlewareStack(                 # AuthMiddlewareStack将使用对当前经过身份验证的用户的引用来填充连接的scope
        URLRouter(
            # chat.routing.websocket_urlpatterns,
            talk.routing.websocket_urlpatterns,
            # kuayu.routing.websocket_urlpatterns,
        )
    ),
})




# 协议类型路由
# ProtocolTypeRouter({
#     "http": some_app,
#     "websocket": some_other_app,
# })
# 网址路由
# URLRouter([
#     url(r"^longpoll/$", LongPollConsumer),
#     url(r"^notifications/(?P<stream>\w+)/$", LongPollConsumer),
#     url(r"", AsgiHandler),
# ])
# 通道名称路由
# ChannelNameRouter({
#     "thumbnails-generate": some_app,
#     "thunbnails-delete": some_other_app,
# })