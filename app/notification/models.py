from django.db import models
from app.user.models import UserAccountTableData

class UserNotificationToken(models.Model):
    user = models.OneToOneField(UserAccountTableData, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'user_notification_token'


class NotificationTable(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField()
    to = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    redirect_to = models.CharField(max_length=255, blank=True)
    publish_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notification'


class NotificationLogTable(models.Model):
    id = models.AutoField(primary_key=True)
    notification = models.ForeignKey(NotificationTable, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccountTableData, on_delete=models.CASCADE)
    readed = models.BooleanField(default=False)

    class Meta:
        db_table = 'notification_log'