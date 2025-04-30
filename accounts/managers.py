from django.contrib.auth.models import BaseUserManager
from accounts import validators, models


class UserManager(BaseUserManager):
    def create_user(self, mobile_number, password=None):
        """
        Creates and saves a User with the given mobile number and password
        """
        if not mobile_number:
            raise ValueError("شماره همراه وارد شود")
        validators.mobile_number_validator(mobile_number)
        user = self.model(mobile_number=mobile_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None):
        """
        Creates and saves a superuser with the given mobile number and password.
        """
        user = self.create_user(
            mobile_number=mobile_number,
            password=password,
        )
        user.is_verified = True
        user.is_active = True
        user.is_superuser = True
        user.user_type = models.UserType.ADMIN
        user.save(using=self._db)
        return user
