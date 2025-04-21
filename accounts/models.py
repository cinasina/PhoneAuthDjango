from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from accounts import validators, managers


class UserType(models.IntegerChoices):
    NORMAL = 1, "کاربر عادی"
    ADMIN = 2, "مدیر"


class User(AbstractBaseUser, PermissionsMixin):
    mobile_number = models.CharField(
        verbose_name="شماره همراه",
        max_length=11,
        validators=[validators.mobile_number_validator],
        unique=True,
    )
    email = models.EmailField(verbose_name="ایمیل", max_length=255, blank=True, null=True, unique=True)
    first_name = models.CharField(verbose_name="نام", max_length=30, blank=True, null=True,)
    last_name = models.CharField(verbose_name="نام خانوادگی", max_length=50, blank=True, null=True,)
    user_type = models.IntegerField(
        verbose_name="نوع کاربر",
        choices=UserType.choices,
        default=UserType.NORMAL.value,
    )
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = managers.UserManager()

    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.mobile_number}"

    def has_perm(self, perm, obj=None):
        return self.user_type == UserType.ADMIN

    def has_module_perms(self, app_label):
        return self.user_type == UserType.ADMIN

    @property
    def is_staff(self):
        return self.user_type == UserType.ADMIN
