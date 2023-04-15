from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import EmailVerifyAPIView, RegistrationAPIView

urlpatterns = [
    path("registration/", RegistrationAPIView.as_view(), name="registration"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "verify/<str:uid>/<str:token>/",
        EmailVerifyAPIView.as_view(),
        name="verify_email",
    ),
]
