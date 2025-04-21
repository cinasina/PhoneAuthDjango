from django.core.validators import RegexValidator
from accounts.messages import Messages

mobile_number_validator = RegexValidator(
    regex=r"^(09[0-9]{9})$",
    message=Messages.MobileNumber.MOBILE_NUMBER_NOT_VALID,
)

otp_validator = RegexValidator(regex=r"^\d{6}$", message=Messages.OTP.OTP_INVALID)
