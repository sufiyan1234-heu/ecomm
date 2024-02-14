from django.conf import settings
from django.core.mail import send_mail


# def send_account_activation_email(email, email_token):
#     subject = "Your account activation"
#     email_from = settings.EMAIL_HOST_USER
#     message = f"Hi, click on the link to activate your account http://127.0.0.1:8000/accounts/activate/{email_token}"
#     send_mail(subject, message, email_from, [email])

# from django.core.mail import send_mail

# send_mail('Test Subject', 'Test Message', 'your-email@example.com', ['recipient@example.com'])
from django.core.mail import EmailMessage


def send_account_activation_email(email, email_token):
    try:
        subject = "Your account activation"
        email_from = settings.EMAIL_HOST_USER
        message = f"Hi, click on the link to activate your account http://127.0.0.1:8000/user/activate/{email_token}"

        # Use EmailMessage for more control
        email_message = EmailMessage(subject, message, email_from, [email])
        email_message.send()

    except Exception as e:
        print(f"Error sending email: {e}")
