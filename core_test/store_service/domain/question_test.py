import unittest
from core.store_service import QuestionFactory, FormQuestion, TextChoiceQuestion, ImageChoiceQuestion
from core.store_service.domain.exceptions import OptionAlreadyExistsException
from ..test_data import DataFactory

class QuestionCreationTest(unittest.TestCase):
    def test_create_form_question(self) -> None:
        for _ in range(10):
            title = DataFactory.store_test_data.get_description()
            input_type = DataFactory.store_test_data.get_input_type()
            with self.subTest(title=title, input_type=input_type):
                form_question = QuestionFactory.create_form_question(title, input_type)
                self.assertIsInstance(form_question, FormQuestion)
                self.assertEqual(form_question.title, title.lower())
                self.assertEqual(form_question.input_type, input_type)
    
    def test_create_text_choice_question(self) -> None:
        for _ in range(10):
            title = DataFactory.store_test_data.get_description()
            with self.subTest(title=title):
                text_choice_question = QuestionFactory.create_text_choice_question(title)
                self.assertIsInstance(text_choice_question, TextChoiceQuestion)
    
    def test_create_image_choice_question(self) -> None:
        for _ in range(10):
            title = DataFactory.store_test_data.get_description()
            with self.subTest(title=title):
                image_choice_question = QuestionFactory.create_image_choice_question(title)
                self.assertIsInstance(image_choice_question, ImageChoiceQuestion)


class TextChoiceQuestionTest(unittest.TestCase):
    questions = DataFactory.generate_text_choice_questions()
    
    def test_add_choice(self) -> None:
        for question in self.questions:
            option = DataFactory.store_test_data.get_description()
            with self.subTest(question=question, option=option):
                question.add_choice(option)
                self.assertIn(option, question.choices)
    
    def test_add_already_exists_choice(self) -> None:
        for question in self.questions:
            option = DataFactory.store_test_data.get_description()
            with self.subTest(question=question, option=option):
                question.add_choice(option)
                with self.assertRaises(OptionAlreadyExistsException):
                    question.add_choice(option)
    
    def test_delete_choice(self) -> None:
        for question in self.questions:
            option = DataFactory.store_test_data.get_description()
            question.add_choice(option)
            with self.subTest(question=question, option=option):
                question.remove_choice(option)
                self.assertNotIn(option, question.choices)


class ImageChoiceQuestionTest(unittest.TestCase):
    questions = DataFactory.generate_image_choice_questions()
    test_folder = 'resources/media/prueba'
    
    def test_add_choice(self) -> None:
        for question in self.questions:
            image = DataFactory.store_test_data.get_sample_base64_images()[0]
            option = DataFactory.store_test_data.get_description()
            with self.subTest(question=question, option=option):
                question.add_choice(option, image)
    
    def test_already_exists_option(self) -> None:
        for question in self.questions:
            image = DataFactory.store_test_data.get_sample_base64_images()[0]
            image2 = DataFactory.store_test_data.get_sample_base64_images()[0]
            option = DataFactory.store_test_data.get_description()
            with self.subTest(option=option):
                question.add_choice(option, image)
                with self.assertRaises(OptionAlreadyExistsException):
                    question.add_choice(option, image2)
    
    def test_delete_choice(self) -> None:
        for question in self.questions:
            image = DataFactory.store_test_data.get_sample_base64_images()[0]
            option = DataFactory.store_test_data.get_description()
            question.add_choice(option, image)
            with self.subTest(question=question, option=option):
                question.remove_choice(option)
                self.assertNotIn(option, question.choices)