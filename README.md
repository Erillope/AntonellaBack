# Proyecto Django

Este es un proyecto desarrollado con Django. A continuación se detallan los pasos necesarios para clonar y ejecutar el proyecto localmente.

## Requisitos previos

- Python 3.8 o superior
- pip (normalmente viene con Python)
- Git (opcional, si vas a clonar desde un repositorio)

## Instalación

1. **Clona el repositorio (opcional):**

   ```bash
   git clone https://github.com/tu-usuario/tu-repo.git
   cd tu-repo
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
