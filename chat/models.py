from django.db import models
from core.models import CustomUser  # Import your CustomUser model

class ChatRoom(models.Model):
    room_name = models.CharField(max_length=100, unique=True)
    participants = models.ManyToManyField(CustomUser)  # Changed from User to CustomUser
    is_group_chat = models.BooleanField(default=False)
    group_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.room_name} ({'Group' if self.is_group_chat else 'Direct'})"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Changed from User to CustomUser
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_group_message = models.BooleanField(default=True)
    recipient = models.ManyToManyField(CustomUser, blank=True, related_name='recipient')  # Changed from User to CustomUser

    def __str__(self):
        return f"{self.sender.username} - {self.timestamp}"