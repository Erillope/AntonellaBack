import subprocess

path = 'core_test'
def test_executer(file: str) -> None:
    subprocess.run(f"python -m unittest {path}/{file}.py", shell=True)

def run_role_test() -> None:
    test_executer('user/domain/role_test')

def run_user_test() -> None:
    test_executer('user/domain/user_test')

def run_mapper_test() -> None:
    test_executer('user/service/mapper_test')
    
def run_role_service_test() -> None:
    test_executer('user/service/role_service_test')

def run_user_service_test() -> None:
    test_executer('user/service/user_service_test')
    
run_user_service_test()