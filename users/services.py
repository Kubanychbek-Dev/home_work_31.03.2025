from django.conf import settings
from django.core.mail import send_mail


def send_register_email(email):
    send_mail(
        subject="Congratulations on registering",
        message="You have successfully registered on our website",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email, ]
    )


def send_new_password(email, new_password):
    send_mail(
        subject="You have successfully changed your password",
        message=f"Your new password is {new_password}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email, ]
    )
