from django.shortcuts import render


def talk(request):
    return render(request, 'talk/index.html')