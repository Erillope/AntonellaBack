import unittest
from core.store_service import StoreServiceFactory, StoreService
from core.store_service.domain.exceptions import InvalidServiceNameException
from ..test_data import DataFactory
from typing import List
from core.common.image_storage import Base64ImageStorage

class StoreServiceCreationTest(unittest.TestCase):        
    def test_store_service_creation(self) -> None:
        for name in DataFactory.store_test_data.get_names():
            description = DataFactory.store_test_data.get_description()
            service_type = DataFactory.store_test_data.get_service_type()
            with self.subTest(name=name, description=description, service_type=service_type):
                service = StoreServiceFactory.create(name=name, description=description, type=service_type)
                self.assertEqual(service.name, name.lower())
                self.assertEqual(service.description, description.lower())
                self.assertEqual(service.type, service_type)

    def test_store_service_create_invalid_name(self) -> None:
        for invalid_name in DataFactory.store_test_data.get_invalid_names():
            description = DataFactory.store_test_data.get_description()
            service_type = DataFactory.store_test_data.get_service_type()
            with self.subTest(invalid_name=invalid_name, description=description, service_type=service_type):
                with self.assertRaises(InvalidServiceNameException):
                    StoreServiceFactory.create(name=invalid_name, description=description, type=service_type)
    
    def test_change_data(self) -> None:
        for store_service, name in zip(DataFactory.generate_store_services(),
                                       DataFactory.store_test_data.get_names()):
            description = DataFactory.store_test_data.get_description()
            service_type = DataFactory.store_test_data.get_service_type()
            status = DataFactory.store_test_data.get_service_status()
            with self.subTest(store_service=store_service, name=name, description=description, 
                              service_type=service_type, status=status):
                store_service.change_data(name=name, description=description, type=service_type, status=status)
                self.assertEqual(store_service.name, name.lower())
                self.assertEqual(store_service.description, description.lower())
                self.assertEqual(store_service.type, service_type)
                self.assertEqual(store_service.status, status)


class StoreServiceTest(unittest.TestCase):
    store_services: List[StoreService] = []
    base64_images: List[str] = []
    test_folder: str = 'resources/media/prueba'
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.store_services = DataFactory.generate_store_services()
        cls.base64_images = DataFactory.store_test_data.get_sample_base64_images()
        
    def test_add_image(self) -> None:
        for store_service, image in zip(self.store_services, self.base64_images):
            len_images = len(store_service.images)
            with self.subTest(store_service=store_service, image=image):  
                store_service.add_image(Base64ImageStorage(folder=self.test_folder, base64_image=image))
                self.assertEqual(len_images+1, len(store_service.images))
    
    def test_delete_image(self) -> None:
        for store_service, image in zip(self.store_services, self.base64_images):
            len_images = len(store_service.images)
            with self.subTest(store_service=store_service):
                base64_image = Base64ImageStorage(folder=self.test_folder, base64_image=image)
                store_service.add_image(base64_image)
                store_service.delete_image(base64_image.get_url())
                self.assertEqual(len_images, len(store_service.images))