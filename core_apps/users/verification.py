from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from datetime import date
import requests
import json
from django.conf import settings
import logging
logger = logging.getLogger("loggers")


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()

class SendEmail():
    def send_verification_email(self, email):
        from .models import User
        user = User.objects.filter(email=email).first()
        subject = "Verify your  account"

        token = account_activation_token.make_token(user)
        # render template mail.txt
        body = render_to_string('mail.html', context={
            'action_url': "http://",
            'user': user,
            'domain': settings.BASE_HOST,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token
        })

        logger.info(f"Sending Verification mail with Sparkpost to email {email} with body {body} and settings.DEFAULT_FROM_EMAIL : {settings.DEFAULT_FROM_EMAIL} and settings.SPARKPOST_API_KEY {settings.SPARKPOST_API_KEY}")

        # set mail to email content with subject, body ,sender and recepient
        # with html content type
        mail = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, to=[email])
        mail.content_subtype = 'html'

        # send email
        mail.send()
        logger.info(f"Mail sent successfully for Verification with Sparkpost to email {email}")
        return ("token", urlsafe_base64_encode(force_bytes(user.pk)))
