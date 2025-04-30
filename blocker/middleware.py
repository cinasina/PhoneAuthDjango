from django.http import HttpResponseForbidden
from blocker import models
from blocker.messages import Messages


class BlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        attempt_users = models.FailedAttempt.objects.filter(ip=ip)
        for attempt_user in attempt_users:
            if attempt_user.is_blocked():
                return HttpResponseForbidden(Messages.BLOCK.TOO_MANY_ATTEMPTS)
        return self.get_response(request)
