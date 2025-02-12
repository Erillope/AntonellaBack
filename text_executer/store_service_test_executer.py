from .text_executer import test_executer, django_test_executer

def run_store_service_test() -> None:
    test_executer('core_test/store_service/store_service_test')
    
def run_store_service_mapper_test() -> None:
    test_executer('core_test/store_service/mapper_test')

def run_store_service_table_mapper_test() -> None:
    django_test_executer('api_test.store_service.table_mapper_test')

def run_store_service_api_test() -> None:
    django_test_executer('api_test.store_service.store_service_api_test')