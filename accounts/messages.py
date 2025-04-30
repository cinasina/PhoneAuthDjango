class Messages:
    class User:
        BANNED = "حساب کاربری غیرفعال است. با پشتیبانی در ارتباط باشید"

    class MobileNumber:
        MISSING = "لطفاً شماره همراه را وارد کنید"
        INVALID = "شماره همراه واردشده معتبر نیست"

    class Password:
        INCORRECT = "رمز عبور نادرست است"
        SET_SUCCESS = "رمز عبور با موفقیت ثبت شد"

    class UserInfo:
        NAME_MISSING = "لطفاً نام را وارد کنید"
        LASTNAME_MISSING = "لطفاً نام خانوادگی را وارد کنید"
        INVALID_EMAIL = "ایمیل واردشده معتبر نیست"
        DUPLICATE_EMAIL = "ایمیل واردشده قبلاً ثبت شده است"
        CREATED_SUCCESS = "اطلاعات کاربری با موفقیت ثبت شد"

    class OTP:
        MISSING = "لطفاً کد تأیید را وارد کنید"
        INVALID = "کد تأیید نامعتبر است"
        VERIFIED = "کد تأیید با موفقیت تأیید شد"

    class Session:
        INVALID = "جلسه نامعتبر است"

    class Block:
        TOO_MANY_ATTEMPTS = "تلاش‌های بیش از حد. لطفاً یک ساعت دیگر امتحان کنید"

    class Login:
        SUCCESSFUL = "با موفقیت وارد شدید"
