from .models import Email, EmailVerificationEvent
from django.core.mail import send_mail
from django.utils import timezone

import config

def email_not_active(email):
    inactive_email = Email.objects.get(email=email, active=False)
    return inactive_email

def create_email_verification(email):
    #get email if exists, create new one if not
    email_obj, _ = Email.objects.get_or_create(email=email)
    obj = EmailVerificationEvent.objects.create(
        parent=email_obj, #foreign key
        email=email
    )
    sent = send_verification_email(obj.id)
    return obj, sent

def verification_message(email_verification, with_html=False):
    if not isinstance(email_verification, EmailVerificationEvent):
        return None
    verify_link =  email_verification.get_link()

    message = {}
    if with_html:
        message['html'] = f"<h1>Click this link to verify your email: </h1><p><a href='{verify_link}'>{verify_link}</a></p>"
    message['text'] = f"Click this link to verify your email: {verify_link}"

    return message

# Performance Tip: execute this task in another thread or as background task. #
def send_verification_email(verification_id):
    verification = EmailVerificationEvent.objects.get(id=verification_id)

    subject = "Verify your email"
    
    email_text = verification_message(verification, True)

    sender = config.get_email_env("EMAIL_HOST_USER")
    recipients = [verification.email]

    # send an verification email
    return send_mail(
        subject,
        email_text['text'],
        sender,
        recipients,
        fail_silently=False,
        html_message=email_text['html']
    )

def verify_token(token, max_attempts=5):
    event = EmailVerificationEvent.objects.get(token=token)

    if not event:
        return False, "Invalid Token", None
    

    token_expired = event.expired_at
    if token_expired.exists():
        return False, "Token expired, try again.", None
    
    max_attempts_reached = event.attempts > max_attempts
    if max_attempts_reached:
        return False, "Token expired due to many retries.", None
    
    # Performance Tip: execute this task in another thread or as background task. #
    event.attempts += 1
    event.last_attempt_at = timezone.now()
    # invalidation process
    if event.attempts > max_attempts:
        event.expired = True
        event.expired_at = timezone.now()
    event.save()
    ##


    email_obj = event.parent # Email.objects.get()
    return True, "Welcome", email_obj