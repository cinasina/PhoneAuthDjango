from rest_framework import generics, status, permissions

from accounts import serializers, logics
from accounts.messages import Messages


class RegisterView(generics.CreateAPIView):
    serializer_class = serializers.MobileNumberSerializer

    def perform_create(self, serializer):
        mobile_number = serializer.validated_data["mobile_number"]
        ip = self.request.META.get("REMOTE_ADDR")
        session_id, next_step = check_user_mobile_number(mobile_number, ip)

        data = {
            "session_id": session_id,
            "next_step": next_step,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class LoginView(generics.CreateAPIView):
    serializer_class = serializers.PasswordSerializer

    def perform_create(self, serializer):
        session_id = serializer.validated_data["session_id"]
        password = serializer.validated_data["password"]
        ip = self.request.META.get("REMOTE_ADDR")
        tokens = check_user_password(session_id, password, ip)

        data = {
            "tokens": tokens,
            "message": Messages.Login.SUCCESSFUL,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class VerifyOTPView(generics.CreateAPIView):
    serializer_class = serializers.OTPSerializer

    def perform_create(self, serializer):
        session_id = serializer.validated_data["session_id"]
        otp = serializer.validated_data["code"]
        ip = self.request.META.get("REMOTE_ADDR")
        next_step = logics.check_otp(session_id, otp, ip)

        data = {
            "session_id": session_id,
            "next_step": next_step,
            "message": Messages.OTP.VERIFIED,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class SetPasswordView(generics.CreateAPIView):
    serializer_class = serializers.PasswordSerializer

    def perform_create(self, serializer):
        session_id = serializer.validated_data["session_id"]
        password = serializer.validated_data["password"]
        next_step = logics.set_password(session_id, password)

        data = {
            "session_id": session_id,
            "next_step": next_step,
            "message": Messages.Password.SET_SUCCESS,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class UserInfoView(generics.CreateAPIView):
    serializer_class = serializers.UserInfoSerializer

    def perform_create(self, serializer):
        session_id = serializer.validated_data["session_id"]
        email = serializer.validated_data.get("email")
        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data["last_name"]
        tokens = logics.complete_user_info(session_id, email, first_name, last_name)

        data = {"tokens": tokens, "message": Messages.UserInfo.CREATED_SUCCESS}
        return Response(data=data, status=status.HTTP_201_CREATED)
