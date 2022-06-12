from django.shortcuts import redirect
from .models import Room, Message
from accounts.models import User

def hostandloginrequired(view_func):

    def wrapper_func(request, *args, **kwargs):
        room = Room.objects.get(slug=kwargs['slug'])

        if not request.user.is_authenticated or  request.user != room.host:
            return redirect("base:room", slug=kwargs['slug'])
        else:
            return view_func(request, *args, **kwargs)


    return wrapper_func  

def userandloginrequired(view_func):

    def wrapper_func(request, *args, **kwargs):
        message = Message.objects.get(pk=kwargs['pk'])

        if not request.user.is_authenticated or  request.user != message.user:
            return redirect("base:room", message.room.slug)
        else:
            return view_func(request, *args, **kwargs)


    return wrapper_func  


def allowchat(view_func):

    def wrapper_func(request, *args, **kwargs):
        room = Room.objects.get(slug=kwargs['slug'])
        user = User.objects.all()
        # print(request.user)

        if not request.user in room.participants.all():
            return redirect("base:room", room.slug)
        else:
            return view_func(request, *args, **kwargs)


    return wrapper_func