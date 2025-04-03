import unittest
from ..test_data import ProductTestData
from core.product import ProductFactory
from core.product.domain.exceptions import InvalidProductNameException
from core.product.domain.values import ProductStatus
from datetime import date

class ProductTest(unittest.TestCase):
    num_tests = 10
    
    def test_create_product(self) -> None:
        for _ in range(self.num_tests):
            data = ProductTestData.product_data()
            with self.subTest():
                product = ProductFactory.create(**data)
                self.assertEqual(product.name, data['name'].lower().strip())
                self.assertEqual(product.service_type, data['service_type'])
                self.assertEqual(product.description, data['description'].lower().strip())
                self.assertEqual(product.price, data['price'])
                self.assertEqual(product.stock, data['stock'])
                self.assertEqual(len(product.images), len(data['images']))
                self.assertEqual(product.status, ProductStatus.ENABLE)
                self.assertEqual(product.created_date, date.today())
                self.assertEqual(product.service_subtype, data['service_subtype'])
                self.assertEqual(product.product_type, data['product_type'])
                self.assertEqual(product.volume, data['volume'])
    
    def test_create_product_with_invalid_name(self) -> None:
        for _ in range(self.num_tests):
            data = ProductTestData.product_data()
            data['name'] = 'I'
            with self.subTest():
                with self.assertRaises(InvalidProductNameException):
                    ProductFactory.create(**data)
    
    def test_change_product_data(self) -> None:
        for _ in range(self.num_tests):
            product = ProductTestData.generate_product()
            stock = product.stock
            new_data = ProductTestData.product_update_data()
        with self.subTest():
            product.change_data(**new_data)
            self.assertEqual(product.name, new_data['name'].lower().strip())
            self.assertEqual(product.service_type, new_data['service_type'])
            self.assertEqual(product.description, new_data['description'].lower().strip())
            self.assertEqual(product.price, new_data['price'])
            self.assertEqual(product.stock, new_data['additional_stock'] + stock)
            self.assertEqual(len(product.images), len(new_data['images']))
            self.assertEqual(product.status, new_data['status'])
            self.assertEqual(product.service_subtype, new_data['service_subtype'])
            self.assertEqual(product.product_type, new_data['product_type'])
            self.assertEqual(product.volume, new_data['volume'])