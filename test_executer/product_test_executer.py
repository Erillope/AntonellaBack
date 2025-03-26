from .test_executer import test_executer, django_test_executer

def run_product_test() -> None:
    test_executer('core_test/product/domain/product_test')

def run_product_api_test() -> None:
    django_test_executer('api_test.product.product_api_test')