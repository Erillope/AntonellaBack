from django.db import models
from app.user.models import UserAccountTableData
from app.store_service.models import QuestionTableData
from app.order.models import ServiceItemTable
from typing import List

class AnswerTableData(models.Model):
    client = models.ForeignKey(UserAccountTableData, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionTableData, on_delete=models.CASCADE)
    service_item = models.ForeignKey(ServiceItemTable, on_delete=models.CASCADE)

    class Meta:
        db_table = "answer"
        constraints = [
            models.UniqueConstraint(fields=['client', 'question', 'service_item'], name='unique_item_question_answer')
        ]

    @classmethod
    def get_question_answer(cls, client_id: str, service_item_id: str, question_id: str) -> str | List[str]:
        answer = cls.objects.get(client__id=client_id, service_item__id=service_item_id, question__id=question_id)
        
        if TextAnswerTableData.objects.filter(id=answer.id).exists():
            return TextAnswerTableData.objects.get(id=answer.id).text
        
        return list(ImageAnswerTableData.objects.filter(id=answer.id).values_list('image', flat=True))
                
class TextAnswerTableData(AnswerTableData):
    text = models.TextField()

    class Meta:
        db_table = "text_answer"


class ImageAnswerTableData(AnswerTableData):
    image = models.CharField(max_length=250)

    class Meta:
        db_table = "image_answer"