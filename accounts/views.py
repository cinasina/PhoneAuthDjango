from rest_framework import generics, status, permissions
from rest_framework.response import Response

from accounts import serializers, logics
from accounts.messages import Messages


class CustomCreateAPIView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.handle_create(serializer, request)

    def handle_create(self, serializer, request):
        raise NotImplementedError("Subclasses must implement handle_create()")


class RegisterView(CustomCreateAPIView):
    serializer_class = serializers.MobileNumberSerializer

    def handle_create(self, serializer, request):
        mobile_number = serializer.validated_data["mobile_number"]
        ip = request.META.get("REMOTE_ADDR")
        session_id, next_step = logics.check_user_mobile_number(mobile_number, ip)

        data = {
            "session_id": session_id,
            "next_step": next_step,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class LoginView(CustomCreateAPIView):
    serializer_class = serializers.MobileLoginSerializer

    def handle_create(self, serializer, request):
        mobile_number = serializer.validated_data["mobile_number"]
        password = serializer.validated_data["password"]
        ip = request.META.get("REMOTE_ADDR")

        tokens = logics.login_with_password(mobile_number, password, ip)

        return Response(
            {"tokens": tokens, "message": Messages.Login.SUCCESSFUL},
            status=status.HTTP_200_OK,
        )


class VerifyOTPView(CustomCreateAPIView):
    serializer_class = serializers.OTPSerializer

    def handle_create(self, serializer, request):
        session_id = serializer.validated_data["session_id"]
        otp = serializer.validated_data["code"]
        ip = request.META.get("REMOTE_ADDR")
        next_step = logics.check_otp(session_id, otp, ip)

        data = {
            "session_id": session_id,
            "next_step": next_step,
            "message": Messages.OTP.VERIFIED,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class SetPasswordView(CustomCreateAPIView):
    serializer_class = serializers.PasswordSerializer

    def handle_create(self, serializer, request):
        session_id = serializer.validated_data["session_id"]
        password = serializer.validated_data["password"]
        next_step = logics.set_password(session_id, password)

        data = {
            "session_id": session_id,
            "next_step": next_step,
            "message": Messages.Password.SET_SUCCESS,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class UserInfoView(CustomCreateAPIView):
    serializer_class = serializers.UserInfoSerializer

    def handle_create(self, serializer, request):
        session_id = serializer.validated_data["session_id"]
        email = serializer.validated_data.get("email")
        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data["last_name"]
        tokens = logics.complete_user_info(session_id, email, first_name, last_name)

        data = {
            "tokens": tokens,
            "message": Messages.UserInfo.CREATED_SUCCESS,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
