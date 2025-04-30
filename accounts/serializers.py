from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.messages import Messages
from accounts import validators, logics

User = get_user_model()


class MobileNumberSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(
        required=True,
        error_messages={"required": Messages.MobileNumber.MISSING},
        validators=[validators.mobile_number_validator],
    )


class PasswordSerializer(serializers.Serializer):
    session_id = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(
        required=True, write_only=True, min_length=8, max_length=70
    )


class MobileLoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(
        required=True,
        error_messages={"required": Messages.MobileNumber.MISSING},
        validators=[validators.mobile_number_validator],
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        max_length=70,
        error_messages={"required": Messages.Password.INCORRECT},
    )


class OTPSerializer(serializers.Serializer):
    session_id = serializers.CharField(required=True, write_only=True)
    code = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={"required": Messages.OTP.MISSING},
        validators=[validators.otp_validator],
    )


class UserInfoSerializer(serializers.ModelSerializer):
    session_id = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            "session_id",
            "email",
            "first_name",
            "last_name",
        )

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                {"message": Messages.UserInfo.DUPLICATE_EMAIL}
            )
        return value

    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError(
                {"message": Messages.UserInfo.NAME_MISSING}
            )
        return value

    def validate_last_name(self, value):
        if not value:
            raise serializers.ValidationError(
                {"message": Messages.UserInfo.LASTNAME_MISSING}
            )
        return value
