from django.db import models
from app.user.models import UserAccountTableData

class ChatTable(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    user = models.OneToOneField(UserAccountTableData, on_delete=models.CASCADE, unique=True)
    
    class Meta:
        db_table = 'chat'

class ChatMessageTable(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    chat = models.ForeignKey(ChatTable, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserAccountTableData, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField()
    message_type = models.CharField(max_length=10)
    
    class Meta:
        ordering = ['timestamp']
        db_table = 'chat_message'