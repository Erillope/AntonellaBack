from app.common.table_mapper import TableMapper
from .models import (StoreServiceTableData, StoreServiceImage, QuestionTableData, QuestionChoice, ChoiceImage,
StoreServicePrice)
from core.store_service import (StoreService, StoreServiceFactory, QuestionFactory, TextChoiceQuestion,
                                ServiceStatus, ServiceType, ImageChoiceQuestion, Question, FormQuestion,
                                Choice)
from core.store_service.service.dto import QuestionInputType
from core.store_service.domain.values import Price

class StoreServiceTableMapper(TableMapper[StoreServiceTableData, StoreService]):
    def to_table(self, store_service: StoreService) -> StoreServiceTableData:
        return StoreServiceTableData(
            id=store_service.id,
            name=store_service.name,
            description=store_service.description,
            status=store_service.status.value,
            type=store_service.type.value,
            duration=store_service.duration,
            subtype=store_service.subtype,
            created_date=store_service.created_date
        )
    
    def to_model(self, store_service_table: StoreServiceTableData) -> StoreService:
        return StoreServiceFactory.load(
            id=str(store_service_table.id),
            name=store_service_table.name,
            description=store_service_table.description,
            status=ServiceStatus(store_service_table.status),
            type=ServiceType(store_service_table.type),
            subtype=store_service_table.subtype,
            duration=store_service_table.duration,
            prices = [
                Price.build(
                    name=price.name,
                    min=price.min_price,
                    max=price.max_price
                ) for price in StoreServicePrice.service_prices(str(store_service_table.id))
            ],
            created_date=store_service_table.created_date,
            images=StoreServiceImage.service_images(str(store_service_table.id))
        )


class QuestionTableMapper(TableMapper[QuestionTableData, Question]):
    def to_table(self, question: Question) -> QuestionTableData:
        if isinstance(question, FormQuestion):
            return QuestionTableData(
                id=question.id,
                title=question.title,
                input_type=question.input_type.value,
                service_id=question.get_store_service(),
                created_date=question.created_date
            )
        return QuestionTableData(
            id=question.id,
            title=question.title,
            input_type=QuestionInputType.CHOICE.value,
            service_id=question.get_store_service(),
            created_date=question.created_date
        )
    
    def to_model(self, question_table: QuestionTableData) -> Question:
        if question_table.input_type == QuestionInputType.CHOICE.value:
            if ChoiceImage.have_choice_images(str(question_table.id)):
                return self._to_image_choice_question(question_table)
            return self._to_text_choice_question(question_table)
        return self._to_form_question(question_table)
    
    def _to_form_question(self, question_table: QuestionTableData) -> FormQuestion:
        return QuestionFactory.load_form_question(
            id=str(question_table.id),
            title=question_table.title,
            input_type=question_table.input_type,
            created_date=question_table.created_date,
            store_service_id=str(question_table.service_id)
        )
    
    def _to_text_choice_question(self, question_table: QuestionTableData) -> TextChoiceQuestion:
        return QuestionFactory.load_text_choice_question(
            id=str(question_table.id),
            title=question_table.title,
            choices=QuestionChoice.question_choices(str(question_table.id)),
            created_date=question_table.created_date,
            store_service_id=str(question_table.service_id)
        )
    
    def _to_image_choice_question(self, question_table: QuestionTableData) -> ImageChoiceQuestion:
        choices = QuestionChoice.question_choices(str(question_table.id))
        return QuestionFactory.load_image_choice_question(
            id=str(question_table.id),
            title=question_table.title,
            choices=[Choice(option=option, image=ChoiceImage.choice_images(str(question_table.id), option)) for option in choices],
            created_date=question_table.created_date,
            store_service_id=str(question_table.service_id)
        )