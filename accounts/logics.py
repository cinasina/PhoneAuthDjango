import random
from uuid import uuid4

from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.messages import Messages
from accounts import tasks
from blocker import logics as blocker_logics

User = get_user_model()


def generate_otp():
    otp = random.randint(100000, 999999)
    if cache.get(f"otp:{otp}"):
        return generate_otp()
    return otp


def generate_jwt_token(user):
    refresh_token = RefreshToken.for_user(user=user)
    access_token = refresh_token.access_token
    return {
        "refresh_token": str(refresh_token),
        "access_token": str(access_token),
    }


def set_session_id(mobile_number):
    session_id = str(uuid4())
    cache.set(session_id, mobile_number, 120)
    return session_id


def get_session_id(session_id):
    user_id = cache.get(session_id)
    if not user_id:
        raise exceptions.ParseError({"message": Messages.Session.INVALID})
    return user_id


def check_user_mobile_number(mobile_number, ip):
    blocker_logics.check_failed_attempts({"ip": ip, "mobile_number": mobile_number})
    try:
        user = User.objects.get(mobile_number=mobile_number)
        if not user.is_verified or not user.is_active:
            raise exceptions.ParseError(
                {"message": Messages.User.NOT_ACTIVATED_VERIFIED}
            )
        return set_session_id(mobile_number), "password"
    except User.DoesNotExist:
        create_user(mobile_number)
        session_id = set_session_id(mobile_number)
        tasks.send_otp(mobile_number)
        return session_id, "otp"


def check_user_password(session_id, password, ip):
    mobile_number = get_session_id(session_id)
    blocker_logics.check_failed_attempts({"ip": ip, "mobile_number": mobile_number})
    user = User.objects.get(mobile_number=mobile_number)
    if user.check_password(password):
        return generate_jwt_token(user)
    raise exceptions.AuthenticationFailed({"message": Messages.Password.INCORRECT})


def create_user(mobile_number):
    return User.objects.create_user(
        mobile_number=mobile_number, is_verified=False, is_active=False
    )


def check_otp(session_id, user_otp, ip):
    mobile_number = get_session_id(session_id)
    blocker_logics.check_failed_attempts({"ip": ip, "mobile_number": mobile_number})
    cached_otp = cache.get(f"otp:{mobile_number}")
    if cached_otp and str(user_otp) == str(cached_otp):
        user = User.objects.get(mobile_number=mobile_number)
        user.is_verified = True
        user.save()
        return "set_password"
    raise exceptions.ParseError({"message": Messages.OTP.INVALID})


def set_password(session_id, password):
    mobile_number = get_session_id(session_id)
    user = User.objects.get(mobile_number=mobile_number)
    user.set_password(password)
    user.is_active = False
    user.save()
    return session_id, "create_user_info"


def complete_user_info(session_id, email, first_name, last_name):
    mobile_number = get_session_id(session_id)
    user = User.objects.get(mobile_number=mobile_number)
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.is_active = True
    user.save()
    return generate_jwt_token(user)
