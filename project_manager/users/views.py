from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import RegistrationSerializer


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
