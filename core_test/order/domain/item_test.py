import unittest
from core.order import ServiceItem
from core.order.domain.values import Progresstatus
from core_test.order.test_data import DataFactory
from datetime import date
from core.common.exceptions import InvalidAmount

class ServiceItemTest(unittest.TestCase):
    def test_create_service_item(self) -> None:
        for _ in range(10):
            service_item = DataFactory.generate_service_items()
            with self.subTest(service_item=service_item):
                self.assertTrue(service_item.date_info.start_time < service_item.date_info.end_time)
                self._validate_price(service_item)
                self._validate_payments(service_item)
                self.assertTrue(service_item.created_date, date.today())
                self.assertTrue(service_item.status, Progresstatus.PENDING)

    def test_create_service_item_with_invalid_percentage(self) -> None:
        for _ in range(10):
            with self.assertRaises(InvalidAmount):
                #crear el servicio con un porcentaje de pago inválido
                pass
    
    def test_create_service_item_with_invalid_date(self) -> None:
        pass
    
    def test_total_payment(self) -> None:
        pass
    
    def test_profits(self) -> None:
        pass
    
    def test_add_employee_payment(self) -> None:
        #Testear que se agregue el payment en la lista de payments y que la información este correcta
        pass
    
    def test_remove_employee_payment(self) -> None:
        pass
    
    def _validate_price(self, service: ServiceItem) -> None:
        sale_price = service.price.sale_price
        expected_sale_price = service.price.base_price * (1 + service.price.iva) + service.price.card_charge
        self.assertTrue(sale_price, expected_sale_price)
    
    def _validate_payments(self, service: ServiceItem) -> None:
        payments = service.payments
        for payment in payments:
            self.assertTrue(payment.amount, service.price.base_price * payment.percentage)