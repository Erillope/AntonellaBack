from django.db import models

class TokenTableData(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    user_id = models.UUIDField()
    created_at = models.DateTimeField()
    expired_at = models.DateTimeField()
    
    class Meta:
        db_table = 'token'