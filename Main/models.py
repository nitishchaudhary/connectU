from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic  =  models.ImageField(default = 'default.jpg',upload_to = 'profile_images')
    about = models.TextField()
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Message(models.Model):
    sender_id = models.ForeignKey(User,related_name="sender",on_delete=models.CASCADE)
    reciever_id = models.ForeignKey(User,related_name="receiver",on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    mesage_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to = 'message_media',blank=True)
