from django.apps import AppConfig
from django.db.models.signals import post_migrate

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.user'
    
    def ready(self) -> None:
        from app.user.config import ServiceConfig
        from django.dispatch import receiver
        
        @receiver(post_migrate)
        def init(sender, **kwargs) -> None:
            ServiceConfig.init()