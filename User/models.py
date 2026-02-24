from django.db import models

from django.contrib.auth.models import User

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    SENDER_CHOICES = [
        ('USER', 'User'),
        ('BOT', 'Bot'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    text = models.TextField()
    sender = models.CharField(max_length=5, choices=SENDER_CHOICES)
    emotion = models.CharField(max_length=20, blank=True, null=True)
    emotion_score = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.sender} - {self.timestamp}"

class EmotionTimeline(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emotion_timeline')
    date = models.DateField()
    positive_score = models.FloatField(default=0.0)
    negative_score = models.FloatField(default=0.0)
    neutral_score = models.FloatField(default=0.0)
    message_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="journals")
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
