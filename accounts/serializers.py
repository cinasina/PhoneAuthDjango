from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model

from accounts.messages import Messages
from accounts import validators

User = get_user_model()


class MobileNumberSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(
        required=True,
        error_messages={"required": Messages.MobileNumber.MOBILE_NUMBER_MISSING},
        validators=[validators.mobile_number_validator],
    )


class PasswordSerializer(serializers.Serializer):
    session_id = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, write_only=True, min_length=8, max_length=70
    )


class OTPSerializer(serializers.Serializer):
    session_id = serializers.CharField(required=True)
    code = serializers.CharField(
        required=True,
        error_messages={"required": Messages.OTP.OTP_MISSING},
        validators=[validators.otp_validator],
    )

class UserInfo(serializers.ModelSerializer):
    session_id = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ("session_id", "email", "first_name", "last_name",)

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"message": Messages.Email.DUPLICATE_EMAIL})
        return value







