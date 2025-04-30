from django.db import models
from django.utils import timezone


class FailedAttempt(models.Model):
    ip = models.GenericIPAddressField(
        verbose_name="IP",
    )
    mobile_number = models.CharField(
        max_length=11,
        null=True,
        blank=True,
    )
    attempts = models.IntegerField(
        default=0,
    )
    last_attempt = models.DateTimeField(
        auto_now=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    blocked_until = models.DateTimeField(
        null=True,
        blank=True,
    )

    def is_blocked(self):
        if self.blocked_until and self.blocked_until > timezone.now():
            return True
        return False
