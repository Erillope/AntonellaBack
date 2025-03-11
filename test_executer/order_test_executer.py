from .test_executer import test_executer

def run_service_item_test() -> None:
    test_executer('core_test/order/domain/item_test')