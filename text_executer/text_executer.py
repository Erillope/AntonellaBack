import subprocess
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "antonella_back.settings")
django.setup()

def test_executer(file: str) -> None:
    subprocess.run(f"python -m unittest {file}.py", shell=True)

def django_test_executer(file: str) -> None:
    subprocess.run(f"python manage.py test {file}", shell=True)