from django.utils.deprecation import MiddlewareMixin
from knox.auth import TokenAuthentication
from django.http import JsonResponse

class AuthenticationMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        auth_token = request.COOKIES.get('auth_token')
        if not auth_token:
            data = {
                "status": False,
                "message": "Unauthorized user token not found",
                "data": auth_token,
            }
            return JsonResponse(data, status=401)
        
        request.META['HTTP_AUTHORIZATION'] = f"Token {auth_token}"

        token_auth = TokenAuthentication()
        user_auth_tuple = token_auth.authenticate(request)
        
        if user_auth_tuple:
            request.user, auth_token = user_auth_tuple
        else:
            data = {
                "status": False,
                "message": "Invalid token",
                "data": auth_token,
            }
            return JsonResponse(data, status=401)

        return None
