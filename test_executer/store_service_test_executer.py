from .test_executer import test_executer, django_test_executer

def run_store_service_test() -> None:
    test_executer('core_test/store_service/domain/store_service_test')

def run_question_test() -> None:
    test_executer('core_test/store_service/domain/question_test')
    
def run_store_service_api_test() -> None:
    django_test_executer('api_test.store_service.store_service_api_test')

def run_question_api_test() -> None:
    django_test_executer('api_test.store_service.question_api_test')