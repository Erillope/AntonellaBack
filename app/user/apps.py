from django.apps import AppConfig
from django.db.models.signals import post_migrate
import sys

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.user'
    
    def ready(self) -> None:
        from app.user.config import ServiceConfig
        if 'runserver' in sys.argv:
            ServiceConfig.init()