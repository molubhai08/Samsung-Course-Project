from django.contrib import admin
from .models import ChatMessage, EmotionTimeline, Journal

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'sender', 'emotion', 'emotion_score', 'timestamp']
    list_filter = ['sender', 'emotion', 'timestamp']
    search_fields = ['text', 'user__username']
    ordering = ['-timestamp']

@admin.register(EmotionTimeline)
class EmotionTimelineAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'positive_score', 'negative_score', 'neutral_score', 'message_count']
    list_filter = ['date']
    search_fields = ['user__username']
    ordering = ['-date']

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ['user', 'date']
    list_filter = ['date']
    search_fields = ['text', 'user__username']
    ordering = ['-date']
