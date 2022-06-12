from django.urls import path
from . import views

app_name = 'base'


urlpatterns = [
    path('', views.index, name='home'),
    path('room/<slug:slug>/', views.room, name='room'),
    path('room/<slug:slug>/chat', views.room_chat, name='room-chat'),

    path('room/<slug:slug>/join/', views.RoomJoin.as_view(), name='room-join'),
    path('room/<slug:slug>/leave/', views.RoomLeave.as_view(), name='room-leave'),
    path('create-room/', views.create_room, name='create-room'),
    path('room/<slug:slug>/update-room/', views.update_room, name='update-room'),
    path('room/<slug:slug>/delete-room/', views.delete_room, name='delete-room'),
    path('room/<int:pk>/delete-message', views.delete_message, name='delete-message'),
    path('topics/', views.topics, name='topics'),
    path('activities/', views.activities, name='activities')

]
