from django.urls import path
from talk import views


urlpatterns = [
    path('room/', views.talk, name='chat-url'),

]