from django.core.cache import cache

from celery import shared_task

from accounts import logics
from services import kavenegar_client


@shared_task()
def send_otp(mobile_number):
    otp = logics.generate_otp()
    kavenegar_client.send_otp_sms(mobile_number=mobile_number, otp=otp)
    cache.set(f"otp:{mobile_number}", otp, 120)
