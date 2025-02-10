import subprocess
import os
import django # type: ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "antonella_back.settings")
django.setup()

def test_executer(file: str) -> None:
    subprocess.run(f"python -m unittest {file}.py", shell=True)

def django_test_executer(file: str) -> None:
    subprocess.run(f"python manage.py test {file}", shell=True)
    
def run_role_test() -> None:
    test_executer('core_test/user/domain/role_test')

def run_user_test() -> None:
    test_executer('core_test/user/domain/user_test')

def run_mapper_test() -> None:
    test_executer('core_test/user/service/mapper_test')
    
def run_role_service_test() -> None:
    test_executer('core_test/user/service/role_service_test')

def run_user_service_test() -> None:
    test_executer('core_test/user/service/user_service_test')

def run_user_table_mapper_test() -> None:
    django_test_executer('api_test.user.table_mapper_test')

def run_role_api_test() -> None:
    django_test_executer('api_test.user.role_api_test')

def run_user_api_test() -> None:
    django_test_executer('api_test.user.user_api_test')
    
def run_all() -> None:
    run_role_test()
    run_user_test()
    run_mapper_test()
    run_role_service_test()
    run_user_service_test()
    run_user_table_mapper_test()
    run_role_api_test()
    run_user_api_test()

run_all()