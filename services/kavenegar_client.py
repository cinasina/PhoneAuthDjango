from django.conf import settings
from kavenegar import *

debug = settings.KAVEHNEGAR_DEBUG
api_key = settings.KAVEHNEGAR_APIKEY


def send_otp_sms(mobile_number, otp):
    if not debug:
        rest_url = "https://api.kavenegar.com/v1/{}/verify/lookup.json".format(api_key)
        headers = {"Content-type": "application/json"}
        params = {"receptor": mobile_number, "token": otp, "template": "verify"}
        try:
            response = requests.get(rest_url, params=params, headers=headers)
            # Raise an exception for non-2xx status codes
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False
    else:
        print(f"Verification Code: {otp}")
