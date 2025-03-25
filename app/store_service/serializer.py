from rest_framework import serializers
from core.store_service import ServiceType, ServiceStatus
from core.store_service.service.dto import (CreateStoreServiceDto, UpdateStoreServiceDto,
                                            QuestionInputType, ChoiceType, CreateQuestionDto, ChoiceDto)
from rest_framework.exceptions import ErrorDetail

class UpdateStoreSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=250, required=False)
    description = serializers.CharField(required=False)
    status = serializers.ChoiceField(choices=[(s.value, s.value) for s in ServiceStatus], required=False)
    type = serializers.ChoiceField(choices=[(t.value, t.value) for t in ServiceType], required=False)
    
    def to_dto(self) -> UpdateStoreServiceDto:
        status = self.validated_data.get('status')
        return UpdateStoreServiceDto(
            id=str(self.validated_data['id']),
            name=self.validated_data.get('name'),
            description=self.validated_data.get('description'),
            status=ServiceStatus(status) if status else None,
            type=ServiceType(self.validated_data['type']) if self.validated_data.get('type') else None
        )


class CreateQuestionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=250)
    input_type = serializers.ChoiceField(choices=[(t.value, t.value) for t in QuestionInputType])
    
    def is_valid(self, *, raise_exception: bool=False) -> bool:
        valid = super().is_valid(raise_exception=raise_exception)
        if not valid: return False
        if self.initial_data.get('input_type') == QuestionInputType.CHOICE.value:
            if not self._is_valid_choice_type(): return False
            if not self._is_valid_choice(): return False
            if not self._is_valid_choice_text(): return False
            if not self._is_valid_choice_image(): return False
        self._validated_data = self.initial_data
        return True

    def to_dto(self) -> CreateQuestionDto:
        choice_type = self.validated_data.get('choice_type')
        choices_data = self.validated_data.get('choices')
        choices = []
        if choice_type == ChoiceType.TEXT.value:
            choices = [ChoiceDto(option=choice) for choice in choices_data]
        elif choice_type == ChoiceType.IMAGE.value:
            choices = [ChoiceDto(option=choice['option'], image=choice['image']) for choice in choices_data]
        return CreateQuestionDto(
            title=self.validated_data['title'],
            input_type=QuestionInputType(self.validated_data['input_type']),
            choice_type=ChoiceType(choice_type) if choice_type else ChoiceType.VOID,
            choices=choices
        )
        
    def _is_valid_choice_type(self) -> bool:
        if 'choice_type' not in self.initial_data:
            self._errors['choice_type'] = [ErrorDetail('This field is required.', code='required')]
            return False
        if self.initial_data.get('choice_type') not in [c.value for c in ChoiceType]:
            self._errors['choice_type'] = [ErrorDetail('Invalid choice type.', code='invalid_choice')]
            return False
        return True
    
    def _is_valid_choice(self) -> bool:
        if 'choices' not in self.initial_data:
            self._errors['choices'] = [ErrorDetail('This field is required.', code='required')]
            return False
        if not isinstance(self.initial_data.get('choices'), list):
            self._errors['choices'] = [ErrorDetail('This field must be a list.', code='invalid_list')]
            return False
        return True
    
    def _is_valid_choice_text(self) -> bool:
        if self.initial_data.get('choice_type') == ChoiceType.TEXT.value:
            for choice in self.initial_data.get('choices'):
                if not isinstance(choice, str):
                    self._errors['choices'] = [ErrorDetail('All choices must be strings.', code='invalid_string')]
                    return False
        return True
    
    def _is_valid_choice_image(self) -> bool:
        if self.initial_data.get('choice_type') == ChoiceType.IMAGE.value:
            for choice in self.initial_data.get('choices'):
                choice_serializer = ChoiceSerializer(data=choice)
                if not choice_serializer.is_valid():
                    self._errors['choices'] = choice_serializer.errors
                    return False
        return True
    
class ChoiceSerializer(serializers.Serializer):
    option = serializers.CharField(max_length=250)
    image = serializers.CharField(required=False)


class PriceSerializar(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    
class CreateStoreSerializer(serializers.Serializer):
    service_id = serializers.UUIDField(required=False)
    name = serializers.CharField(max_length=250)
    description = serializers.CharField()
    type = serializers.ChoiceField(choices=[(t.value, t.value) for t in ServiceType])
    duration = serializers.TimeField()
    prices = serializers.ListField(child=PriceSerializar())
    images = serializers.ListField(child=serializers.CharField())
    questions = serializers.ListField(child=CreateQuestionSerializer())
    
    def is_valid(self, *, raise_exception: bool=False) -> bool:
        valid = super().is_valid(raise_exception=raise_exception)
        if not valid: return False
        for question in self.initial_data['questions']:
            question_serializer = CreateQuestionSerializer(data=question)
            if not question_serializer.is_valid():
                self._errors['questions'] = question_serializer.errors
                return False
        self._validated_data = self.initial_data
        return True
    
    def to_dto(self) -> CreateStoreServiceDto:
        question_dto = []
        for question in self.validated_data['questions']:
            question_serializer = CreateQuestionSerializer(data=question)
            question_serializer.is_valid()
            question_dto.append(question_serializer.to_dto())
        return CreateStoreServiceDto(
            name=self.validated_data['name'],
            description=self.validated_data['description'],
            type=ServiceType(self.validated_data['type']),
            images=self.validated_data['images'],
            questions=question_dto,
            duration=self.validated_data['duration'],
            prices=self.validated_data['prices']
        )


class UpdateQuestion(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=250, required=False)