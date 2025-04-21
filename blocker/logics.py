from django.utils.timezone import timezone, timedelta
from rest_framework import exceptions

from blocker import models
from blocker.messages import Messages

def check_failed_attempts(ip, max_attempts=3, block_duration=3600):
    attempt, created = models.FailedAttempt.objects.get_or_create(ip=ip, defaults={"attempts": 0})
    if attempt.is_blocked():
        raise exceptions.ParseError({"message": Messages.BLOCK.TOO_MANY_ATTEMPTS})
    attempt.attempts += 1
    if attempt.attempts >= max_attempts:
        attempt.blocked_until = timezone.now() + timezone.timedelta(seconds=block_duration)
    attempt.save()
    return attempt