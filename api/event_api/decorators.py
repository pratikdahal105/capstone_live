from asyncio.windows_events import NULL
from django.http import JsonResponse
from functools import wraps
from registration.models import Profile

def check_user_status(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": False,
                "message": "User is not authenticated",
                "data": None
            }, status=403)

        try:
            profile = Profile.objects.get(user=request.user)

            if profile.status <= 1:
                return view_func(request, *args, **kwargs)
            else:
                return JsonResponse({
                    "status": False,
                    "message": "Access denied.",
                    "data": None
                }, status=403)
        except Profile.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Profile does not exist",
                "data": None
            }, status=403)

    return _wrapped_view