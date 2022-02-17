from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic  =  models.ImageField(default = 'default.jpg',upload_to = 'profile_images')
    about = models.TextField()
    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender_id = models.ForeignKey(User,related_name="sender",on_delete=models.CASCADE)
    reciever_id = models.ForeignKey(User,related_name="receiver",on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    mesage_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to = 'message_media',blank=True)

