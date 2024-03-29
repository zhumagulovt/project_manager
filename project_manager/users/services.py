from django.utils import timezone

from .models import User


def activate_user(user: User) -> None:
    user.is_active = True
    # to make used token invalid
    user.last_login = timezone.now()
    user.save(update_fields=["is_active"])


def change_password(user: User, password: str) -> None:
    user.set_password(password)
    user.save(update_fields=["password"])
