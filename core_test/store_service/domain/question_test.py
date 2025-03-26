import unittest
from core.store_service import QuestionFactory, FormQuestion, TextChoiceQuestion, ImageChoiceQuestion, InputType, Choice
from core.store_service.domain.exceptions import OptionAlreadyExistsException
from ..test_data import StoreTestData
import lorem # type: ignore
from core_test.images_data import get_base64_string
import random

class QuestionCreationTest(unittest.TestCase):
    num_tests = 10
    
    def test_create_form_question(self) -> None:
        for _ in range(self.num_tests):
            title = lorem.sentence()
            input_type = random.choice(list(InputType))
            with self.subTest(title=title, input_type=input_type):
                question = QuestionFactory.create_form_question(title=title, input_type=input_type)
                self.assertEqual(question.title, title.lower().strip())
                self.assertEqual(question.input_type, input_type)
    
    def test_create_text_choice_question(self) -> None:
        for _ in range(self.num_tests):
            title = lorem.sentence()
            choices = [lorem.sentence() for _ in range(3)]
            with self.subTest(title=title, choices=choices):
                question = QuestionFactory.create_text_choice_question(title=title, choices=choices)
                self.assertEqual(question.title, title.lower().strip())
                self.assertEqual(question.choices, choices)
    
    def test_create_image_choice_question(self) -> None:
        for _ in range(self.num_tests):
            title = lorem.sentence()
            choices = [
                Choice(
                    option=lorem.sentence(),
                    image=get_base64_string()
                ) for _ in range(3)
            ]
            with self.subTest(title=title):
                question = QuestionFactory.create_image_choice_question(title=title, choices=choices)
                self.assertEqual(question.title, title.lower().strip())
                self.assertEqual([c.option for c in question.choices], [c.option for c in choices])
                self.assertEqual(len(question.choices), len(choices))