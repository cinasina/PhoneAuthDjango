from django.utils import timezone
from datetime import timedelta

from rest_framework import exceptions

from blocker import models
from blocker.messages import Messages


def check_failed_attempts(identifier, max_attempts=3, block_duration=3600):
    ip = identifier["ip"]
    attempt, created = models.FailedAttempt.objects.get_or_create(
        ip=ip,
        defaults={"attempts": 0, "mobile_number": identifier.get("mobile_number", "")},
    )
    if attempt.is_blocked():
        raise exceptions.ParseError({"message": Messages.BLOCK.TOO_MANY_ATTEMPTS})
    attempt.attempts += 1
    if attempt.attempts >= max_attempts:
        attempt.blocked_until = timezone.now() + timedelta(seconds=block_duration)
    attempt.mobile_number = identifier.get("mobile_number", "")
    attempt.save()
    return attempt
