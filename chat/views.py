from django.shortcuts import render



def index(request):
    return render(request, 'enter_room.html', {})


def room(request, room_name):
    return render(request, 'room.html', {'room_name': room_name})

