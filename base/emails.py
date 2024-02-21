from django.conf import settings
from django.core.mail import send_mail


def send_account_activation_email(email, email_token):
    subject = "Email Verification for Bazaar"
    email_from = settings.EMAIL_HOST_USER
    message = f"Hi, click on this link tp activate your account. http://127.0.0.1:8000/account/activate/{email_token}"
    try:
        send_mail(subject, message, email_from, [email])
        return True
    except Exception as e:
        return False
