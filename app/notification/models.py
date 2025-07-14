from django.db import models
from app.user.models import UserAccountTableData

class UserNotificationToken(models.Model):
    user = models.OneToOneField(UserAccountTableData, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'user_notification_token'
