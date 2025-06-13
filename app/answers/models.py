from django.db import models
from app.user.models import UserAccountTableData
from app.store_service.models import QuestionTableData
from app.order.models import ServiceItemTable

class AnswerTableData(models.Model):
    client = models.ForeignKey(UserAccountTableData, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionTableData, on_delete=models.CASCADE)
    service_item = models.ForeignKey(ServiceItemTable, on_delete=models.CASCADE)

    class Meta:
        db_table = "answer"
        constraints = [
            models.UniqueConstraint(fields=['client', 'question', 'service_item'], name='unique_item_question_answer')
        ]

class TextAnswerTableData(AnswerTableData):
    text = models.TextField()

    class Meta:
        db_table = "text_answer"


class ImageAnswerTableData(AnswerTableData):
    images = models.CharField(max_length=250)

    class Meta:
        db_table = "image_answer"