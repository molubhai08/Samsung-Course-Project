from django.db import models

from django.contrib.auth.models import User

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):

    SENDER_CHOICES = [
        ('USER', 'User'),
        ('BOT', 'Bot'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField()

    sender = models.CharField(
        max_length=5,
        choices=SENDER_CHOICES
    )

    emotion = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user} - {self.sender}"

class EmotionTimeline(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.DateField()

    dominant_emotion = models.CharField(
        max_length=20
    )

    average_score = models.FloatField()

    def __str__(self):
        return f"{self.user} - {self.date}"
    
class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="journals")
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
