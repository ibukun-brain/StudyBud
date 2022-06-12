from django.db import models
from django.forms import SlugField
from accounts.models import User
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    id = models.AutoField(primary_key=True) 
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)


    class Meta:
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("base:room", kwargs={"slug": self.slug})




class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return self.body[0:50]
    
    

def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Room.objects.filter(slug=slug).order_by('-pk')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().pk)
        return create_slug(instance, new_slug=new_slug)

    return slug


def pre_save_room_reciever(sender, instance, *args, **kwargs):

    if not instance.slug:
        instance.slug = create_slug(instance)
pre_save.connect(pre_save_room_reciever, sender=Room)
