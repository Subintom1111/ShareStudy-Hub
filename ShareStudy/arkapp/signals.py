from django.core.mail import send_mail
from django.conf import settings


message="Welcome to ShareStUDY HUB"
subject="helllo"


send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
)