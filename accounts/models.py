from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

def profile_pic(instance, filename):
    filefolder ='profile_photos'
    return f"{filefolder}/{instance.username}/{filename}"

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(default='avatar.svg', null=True, upload_to=profile_pic)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.username
    

def create_slug(instance, new_slug=None):
    slug = slugify(instance.username)
    if new_slug is not None:
        slug = new_slug
    qs = User.objects.filter(slug=slug).order_by('-pk')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().pk)
        return create_slug(instance, new_slug=new_slug)

    return slug


def pre_save_room_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_room_reciever, sender=User)
