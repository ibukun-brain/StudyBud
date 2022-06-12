from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from base.decorators import allowchat, hostandloginrequired
from base.forms import RoomModelForm
from .models import Topic, Room, Message
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from accounts.models import User

# Create your views here.

def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    print(q)
    
    topics = Room.objects.values('topic__name').annotate(Count('topic__name')).order_by('-topic__name__count')[:5]
    total_topics = Room.objects.aggregate(Count('topic'))
    rooms = Room.objects.filter(
                Q(topic__name__icontains=q)|
                Q(name__icontains=q)|
                Q(description__icontains=q)
        ).distinct()

    messages = Message.objects.filter(
            Q(room__topic__name__icontains=q)|
            Q(room__name__icontains=q)
    ).distinct()[:4]

    context = {
        'topics':topics,
        'total_topics':total_topics,
        'rooms':rooms,
        'messages':messages,
    }

    return render(request, 'base/index.html', context)

@login_required(login_url='accounts:login')
def room(request, slug):
    room = Room.objects.get(slug=slug)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    context = {
        'room':room,
        'room_messages': room_messages,
        'participants':participants,
    }

    return render(request, 'base/room_join.html', context)


@allowchat
def room_chat(request, slug):
    room = Room.objects.get(slug=slug)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        body = request.POST['body']

        Message.objects.create(
            user = request.user,
            room = room,
            body = body
        )

        # room.participants.add(request.user)
        return redirect('base:room-chat', room.slug)

    context = {
        'room':room,
        'room_messages': room_messages,
        'participants':participants,
    }

    return render(request, 'base/room.html', context)


def delete_message(request, pk):

    message = Message.objects.get(pk=pk)

    message.delete()
# 
    return redirect(request.META['HTTP_REFERER'])
    # return HttpResponse('')

class RoomJoin(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        room = Room.objects.get(slug=kwargs['slug'])
        room.participants.add(self.request.user)

        return reverse_lazy('base:room-chat', kwargs={'slug':kwargs['slug']})


class RoomLeave(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        room = Room.objects.get(slug=kwargs['slug'])
        room.participants.remove(self.request.user)

        return reverse_lazy('base:home')

        
        # return super(RoomJoin, self).get_redirect_url(*args, **kwargs)




@login_required(login_url='accounts:login')
def create_room(request):
    title = 'Create'
    topics = Topic.objects.all()

    if request.method == 'POST':
        room_topic = request.POST['topic']
        room_name = request.POST['room_name']
        room_description = request.POST['room_about']
        print(room_topic)
        
        topic, created = Topic.objects.get_or_create(name=room_topic)

        room  = Room.objects.create(
            host = request.user,
            name = room_name,
            topic = topic,
            description = room_description,
        )
        # room.participants.add(request.user)
        return redirect('base:home')


        # if form.is_valid():
            # Room.objects.create(
                # ''
            # )


    context = {
        'topics':topics,
        'title':title
    }
    

    return render(request, 'base/room_form.html', context)

@hostandloginrequired
def update_room(request, slug):
    title = 'Update'
    topics = Topic.objects.all()
    room = Room.objects.get(slug=slug)

    # form = RoomModelForm(request.POST or None, instance=room)

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('room_name')
        room.topic = topic
        room.description = request.POST.get('room_about')
        room.save()
        return redirect('base:room', room.slug)
    

    context = {
        'topics':topics,
        'title':title,
        # 'form':form,
        'room':room,
    }
    

    return render(request, 'base/room_form.html', context)

@hostandloginrequired
def delete_room(request, slug):
    room = Room.objects.get(slug=slug)

    room.delete()

    return redirect('base:home')



def topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Room.objects.filter(topic__name__icontains=q).values('topic__name').annotate(Count('topic__name')).order_by('-topic__name__count')[:5]
    total_topics = Room.objects.filter(topic__name__icontains=q).aggregate(Count('topic'))

    context = {
        'topics':topics,
        'total_topics':total_topics,
        'q':q,
    }


    return render(request, 'base/topics.html', context)



def activities(request):

    messages = Message.objects.all()

    context = {
        'messages':messages
    }

    return render(request, 'base/activities.html', context)