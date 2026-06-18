from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_participants', 'created_at', 'updated_at']

    def get_participants(self, obj):
        return ', '.join(u.username for u in obj.participants.all())
    get_participants.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'conversation', 'text', 'is_read', 'created_at']
    list_filter = ['is_read']
