from django.urls import path

from rest_framework_simplejwt.views import (  # isort:skip
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (  # isort:skip
    ChangePasswordAPIView,
    EmailVerifyAPIView,
    RegistrationAPIView,
    ResetPasswordAPIView,
    ResetPasswordCompleteAPIView,
)

urlpatterns = [
    path("registration/", RegistrationAPIView.as_view(), name="registration"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "verify/<str:uid>/<str:token>/",
        EmailVerifyAPIView.as_view(),
        name="verify_email",
    ),
    path(
        "change-password/",
        ChangePasswordAPIView.as_view(),
        name="change_password",
    ),
    path(
        "reset-password/",
        ResetPasswordAPIView.as_view(),
        name="reset_password",
    ),
    path(
        "reset-password-complete/",
        ResetPasswordCompleteAPIView.as_view(),
        name="reset_password_complete",
    ),
]
