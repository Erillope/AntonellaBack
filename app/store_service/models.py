from django.db import models #type: ignore
from core.store_service import ServiceType, ServiceStatus
from typing import List
from core.store_service.service.dto import QuestionInputType

class StoreServiceTableData(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=[(s.value, s.value) for s in ServiceStatus])
    type = models.CharField(max_length=50, choices=[(t.value, t.value) for t in ServiceType])
    created_date = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'store_service'
        
        
class StoreServiceImage(models.Model):
    image = models.TextField()
    service = models.ForeignKey(StoreServiceTableData, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'store_service_image'

    @classmethod
    def service_images(cls, service_id: str) -> List[str]:
        return [image.image for image in cls.objects.filter(service__id=service_id)]
    

class QuestionTableData(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    title = models.TextField()
    input_type = models.CharField(max_length=50, choices=[(t.value, t.value) for t in QuestionInputType])
    service = models.ForeignKey(StoreServiceTableData, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'store_service_question'
    
    @classmethod
    def service_questions(cls, service_id: str) -> List['QuestionTableData']:
        return cls.objects.filter(service__id=service_id)


class QuestionChoice(models.Model):
    option = models.TextField()
    question = models.ForeignKey(QuestionTableData, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'question_choice'
    
    @classmethod
    def question_choices(cls, question_id: str) -> List[str]:
        return [choice.option for choice in cls.objects.filter(question__id=question_id)]


class ChoiceImage(models.Model):
    image = models.TextField()
    choice = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'question_image'
    
    @classmethod
    def choice_images(cls, question_id: str, option: str) -> str:
        return cls.objects.get(choice__question_id=question_id, choice__option=option).image
    
    @classmethod
    def have_choice_images(cls, question_id: str) -> bool:
        return cls.objects.filter(choice__question_id=question_id).count() > 0