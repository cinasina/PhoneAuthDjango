from django.http import HttpResponseForbidden
from blocker import models
from blocker.messages import Messages

class BlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')

        try:
            attempt_user = models.FailedAttempt.objects.get(ip=ip)
            if attempt_user.is_blocked():
                return HttpResponseForbidden(Messages.BLOCK.TOO_MANY_ATTEMPTS)
        except models.FailedAttempt.DoesNotExist:
            pass

        return self.get_response(request)


