import random

from django.conf import settings
from django.core.mail import EmailMessage, send_mail

from .models import User, OneTimePassword


def generateOtp():
    otp = ""
    for i in range(6):
        otp += str(random.randint(1, 9))
    return otp


def send_code_to_user(email):
    Subject = "One time passcode for Email verification"
    otp_code = generateOtp()
    print(otp_code)
    user = User.objects.get(email=email)
    current_site = "ambanimasoMamiratra.com"
    email_body = f'Hi {user.first_name} thanks for signing up on {current_site} please verify your email with code {otp_code}.'
    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(user=user, code=otp_code)
    d_email = EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email])
    d_email.send(fail_silently=True)


def send_code_to_user_email(email):
    Subject = "Activate your account."
    otp_code = generateOtp()
    print(otp_code)
    user = User.objects.get(email=email)
    current_site = "agribusiness.com"
    OneTimePassword.objects.create(user=user, code=otp_code)
    send_mail(
        subject=Subject,
        message=f'Hi {user.first_name} thanks for signing up on {current_site} please verify your email with code '
                f'{otp_code}.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True,

    )


def resend_code_to_user_email(code, email):
    Subject = "Activate your account."
    print("your code is " + code)
    user = User.objects.get(email=email)
    current_site = "agribusiness.com"
    send_mail(
        subject=Subject,
        message=f'Hi {user.first_name} thanks for signing up on {current_site} please verify your email with code '
                f'{code}.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True,

    )


def send_notification_of_creation_to_user_email(name, email):
    Subject = "Creation de compte."
    print(f"Email sended to {email}")
    current_site = "agribusiness.com"
    send_mail(
        subject=Subject,
        message=f'Hi {name} your account in {current_site} already created by administrator!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True,

    )


def send_answer_to_visitor_email(name, email):
    Subject = "Thanks for visitor."
    print(f"Email sended to {email}")
    current_site = "agribusiness.com"
    send_mail(
        subject=Subject,
        message=f'Hi {name}!\nThank you for visiting and giving message for our website {current_site}, please join use to show the more '
                f'activities.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True,

    )


def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send()
