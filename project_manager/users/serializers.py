from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core import exceptions
from rest_framework import serializers
from rest_framework.settings import api_settings

from .utils import get_user_by_uid, send_email_confirmation_link

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registration"""

    password_confirm = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "password_confirm",
        ]

    def validate(self, data):
        """
        Check password and password_validation
        Validate password with django's default validators
        """

        password_confirm = data.pop("password_confirm", None)

        if data["password"] != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "Password confirmation is wrong"}
            )

        # password validation
        user = User(**data)
        password = data.get("password")

        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {
                    "password": serializer_error[
                        api_settings.NON_FIELD_ERRORS_KEY
                    ]
                }
            )

        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_email_confirmation_link(user, self.context["request"])
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing user's password"""

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        user = self.context.get("user")

        if not user.check_password(current_password):
            raise serializers.ValidationError(
                {"current_password": "Current password is invalid"}
            )

        if current_password == new_password:
            raise serializers.ValidationError(
                {"new_password": "New password is similar to current"}
            )

        # password validation
        try:
            validate_password(new_password, user)
        except exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {
                    "new_password": serializer_error[
                        api_settings.NON_FIELD_ERRORS_KEY
                    ]
                }
            )

        return data


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for sending email to reset password"""

    email = serializers.CharField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"email": "Invalid email"})
        return value


class ResetPasswordCompleteSerializer(serializers.Serializer):
    """Serializer for completing password reset"""

    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        password = data.get("password")
        password_confirm = data.get("password_confirm")

        try:
            user = get_user_by_uid(data.get("uid"))

            # add the user to data, whose password needs to be reset
            # we need to get user in views
            data["user"] = user

        except (ValueError, TypeError, User.DoesNotExist):
            raise serializers.ValidationError({"uid": "Invalid uid"})

        if not default_token_generator.check_token(
            user=user, token=data.get("token")
        ):
            raise serializers.ValidationError({"token": "Invalid token"})

        # password validation
        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {
                    "password": serializer_error[
                        api_settings.NON_FIELD_ERRORS_KEY
                    ]
                }
            )

        # password confirm validation
        if password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords aren't match"}
            )

        return data


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]
