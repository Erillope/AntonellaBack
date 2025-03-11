from core.common.email import EmailHost, EmailMessage
from core.common.config import AppConfig
from django.core.mail import EmailMessage as Message
from django.core.mail.backends.smtp import EmailBackend
from core.user.domain.values import UserEmail

class DjangoEmailHost(EmailHost):
    def __init__(self) -> None:
        self.set_host(AppConfig.default_super_admin().get('email', ''), AppConfig.email_password())
    
    def send_email(self, message: EmailMessage) -> None:
        email = self._create_message(message)
        email.connection = self.custom_backend
        email.send()
    
    def _create_message(self, message: EmailMessage) -> Message:
        UserEmail.validate(message.to.lower())
        return Message(
            subject=message.subject,
            body=message.body,
            to=[message.to],
            from_email=self.email_host
        )
        
    def set_host(self, email_host: str, password: str) -> None:
        UserEmail.validate(email_host.lower())
        self.email_host = email_host
        self.password = password
        self.custom_backend = EmailBackend(
            host="smtp.gmail.com",
            port=587,
            username=self.email_host,
            password=self.password,
            use_tls=True,
            fail_silently=False,
        )