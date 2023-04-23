from django.contrib.auth.tokens import default_token_generator
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import User
from .serializers import RegistrationSerializer
from .services import activate_user
from .utils import get_user_by_uid


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
