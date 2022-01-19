from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.process_request(request)
        return response

    @staticmethod
    def process_request(request):
        if hasattr(request, "user"):
            user = request.user
        if user.is_authenticated:
            user.last_request_time = timezone.now()
            user.save()
