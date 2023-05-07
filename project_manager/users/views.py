from django.contrib.auth.tokens import default_token_generator
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import (
    ChangePasswordSerializer,
    RegistrationSerializer,
    ResetPasswordSerializer,
)
from .services import activate_user, change_password
from .utils import get_user_by_uid, send_reset_password_link


class RegistrationAPIView(GenericAPIView):
    """
    Registration endpoint
    """

    serializer_class = RegistrationSerializer
    authentication_classes = ()

    success_message = "New user was successfully created"

    @extend_schema(
        responses={201: OpenApiResponse(description=success_message)}
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)

        return Response(self.success_message, status=status.HTTP_201_CREATED)


class EmailVerifyAPIView(GenericAPIView):
    def get(self, request, uid, token):
        try:
            user = get_user_by_uid(uid)
        except (ValueError, TypeError, User.DoesNotExist):
            return Response("Bad uid", status=400)

        if default_token_generator.check_token(user, token):
            activate_user(user)

            return Response(200)

        return Response("Bad token", status=400)


class ChangePasswordAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        data = request.data
        user = request.user
        serializer = self.get_serializer(data=data, context={"user": user})
        serializer.is_valid(raise_exception=True)

        change_password(user, serializer.validated_data.get("new_password"))

        return Response(
            "Password successfully changed", status=status.HTTP_200_OK
        )


class ResetPasswordAPIView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data.get("email"))
        send_reset_password_link(user)
        return Response(
            "Link to reset password was sent to email",
            status=status.HTTP_200_OK,
        )
