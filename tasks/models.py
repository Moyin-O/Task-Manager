# tasks/models.py
# tasks/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

class Task(models.Model):
    title = models.CharField(max_length=255)
    deadline = models.DateTimeField()
    description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=True)

@receiver(post_save, sender=Task)
def send_deadline_notification(sender, instance, **kwargs):
    notification_timeframe = timezone.timedelta(days=1)
    now = timezone.now()
    deadline_difference = instance.deadline - now
