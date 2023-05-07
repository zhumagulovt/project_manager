from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User
from .tasks import (
    send_email_confirmation_link_task,
    send_reset_password_link_task,
)


def send_email_confirmation_link(user: User, request: HttpRequest) -> None:
    """Send to new user confirmation link to verify email"""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verification_link = request.build_absolute_uri(
        reverse("verify_email", kwargs={"uid": uid, "token": token})
    )
    send_email_confirmation_link_task.delay(
        user_email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        verification_link=verification_link,
    )


def send_reset_password_link(user: User) -> None:
    """Send to user link for resetting password"""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_password_link = (
        settings.RESET_PASSWORD_LINK + f"?uid={uid}&token={token}"
    )

    send_reset_password_link_task.delay(
        user_email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        reset_password_link=reset_password_link,
    )


def get_user_by_uid(uid: str) -> User:
    """Get user by uid64"""

    pk = force_str(urlsafe_base64_decode(uid))
    user = User.objects.get(pk=pk)

    return user
