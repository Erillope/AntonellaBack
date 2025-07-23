from django.db import models
from app.user.models import UserAccountTableData
from app.store_service.models import StoreServiceTableData

class CommentTable(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    starts = models.IntegerField()
    user = models.ForeignKey(UserAccountTableData, on_delete=models.CASCADE)
    service = models.ForeignKey(StoreServiceTableData, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comment_table'