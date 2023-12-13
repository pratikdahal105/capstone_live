from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .decorators import require_authenticated_and_valid_token as valid_token
from .serializers import UserRegistrationSerializer, UserProfileUpdateSerializer, PasswordChangeSerializer
from knox.auth import AuthToken
from django.contrib.auth.models import User
from registration.models import Token
import jwt
import random
import string
from django.http import JsonResponse
from datetime import datetime
from django.conf import settings
from django.utils.timezone import now
from .mail import verification_token, send_verification_email, send_password_email
import json
from django.http import JsonResponse

@api_view(["GET"])
def test(request):
    data = {"status": True, "message": "Testing API", "data": None}
    return Response(data)


@api_view(["POST"])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]

    _, token = AuthToken.objects.create(user)

    data = {"status": True, "message": "Login Successfull", "data": {"token": token}}
    response = Response(data, status=200)
    response.set_cookie('auth_token', token, httponly=True, secure=True, samesite='None', max_age=7*24*60*60)
    return response

@valid_token
@api_view(["GET"])
def get_user_data(request):
    user = request.user
    profile = user.profile
    data = {
        "status": True,
        "message": "Authenticated user info",
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": profile.phone,
            "status": profile.status
        },
    }

    return Response(data, status=200)


@api_view(["POST"])
def registration_api(request):
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        _, token = AuthToken.objects.create(user)

        token = verification_token(user)
        send_verification_email(user, token)
        data = {
            "status": True,
            "message": "Registration Successful",
            "data": {"user_id": user.id, "token": token},
        }
        return Response(data, status=201)

    errors = serializer.errors
    data = {
        "status": False,
        "message": "Registration Failed",
        "data": {"errors": errors},
    }
    return Response(data, status=400)

@api_view(["PUT"])
@valid_token
def update_profile(request):
    user = request.user
    serializer = UserProfileUpdateSerializer(user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        data = {
            "status": True,
            "message": "Profile Updated Successfully",
        }
        return Response(data, status=200)

    errors = serializer.errors
    data = {
        "status": False,
        "message": "Profile Update Failed",
        "data": {"errors": errors},
    }
    return Response(data, status=400)

@api_view(["PUT"])
@valid_token
def change_password(request):
    user = request.user
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        data = {
            "status": True,
            "message": "Password changed successfully",
        }
        return Response(data, status=200)

    errors = serializer.errors
    data = {
        "status": False,
        "message": "Password change failed",
        "data": {"errors": errors},
    }
    return Response(data, status=400)

@api_view(["GET"])
def verify_email(request):
    data = json.loads(request.body)
    token = request.GET.get('token')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'], email=payload['email'])
        profile = user.profile
        profile.verified_at = datetime.now()
        profile.save()
        return JsonResponse({"status": True, "message": "Email verified successfully"})
    except jwt.ExpiredSignatureError:
        return JsonResponse({"status": False, "message": "Token has expired"})
    except jwt.InvalidTokenError:
        return JsonResponse({"status": False, "message": "Invalid token"})
    except User.DoesNotExist:
        return JsonResponse({"status": False, "message": "User does not exist"})


@api_view(["POST"])
def forgot_password(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')

        if email:
            try:
                user = User.objects.get(email=email)
                chars = string.ascii_uppercase + string.digits
                token = ''.join(random.choice(chars) for _ in range(6))
                send_password_email(user, token)
                return JsonResponse({"status": True, "message": "Email sent successfully"})
            except User.DoesNotExist:
                return JsonResponse({"status": False, "message": 'User not found'})
        else:
            return JsonResponse({"status": False, "message": 'Email parameter not provided'})
    except json.JSONDecodeError:
        return JsonResponse({"status": False, "message": 'Invalid JSON data'})
    
@api_view(["POST"])
def validate_token(request):
    try:
        data = json.loads(request.body)
        token = data.get('token')

        if token:
            try:
                token_model = Token.objects.get(token=token)
                current_datetime = now()
                if current_datetime < token_model.valid_till:
                    return JsonResponse({"status": True, "message": 'Valid Token'})
                else:
                    return JsonResponse({"status": False, "message": 'Token Expired'})
            except Token.DoesNotExist:
                return JsonResponse({"status": False, "message": 'Invalid Token'})
        else:
            return JsonResponse({"status": False, "message": 'Token Required'})
    except json.JSONDecodeError:
        return JsonResponse({"status": False, "message": 'Invalid JSON data'})
    
@api_view(["POST"])
def update_password(request):
    try:
        data = json.loads(request.body)
        token = data.get('token')
        new_password = data.get('password')

        if not token:
            return JsonResponse({"status": False, "message": 'Token Required'})

        if not new_password:
            return JsonResponse({"status": False, "message": 'New password is required'})

        try:
            token_model = Token.objects.get(token=token)
            current_datetime = now()

            if current_datetime >= token_model.valid_till:
                return JsonResponse({"status": False, "message": 'Token Expired'})

            user = token_model.user
            user.set_password(new_password)
            user.save()

            token_model.delete()

            return JsonResponse({"status": True, "message": 'Password updated successfully'})

        except Token.DoesNotExist:
            return JsonResponse({"status": False, "message": 'Invalid Token'})

    except json.JSONDecodeError:
        return JsonResponse({"status": False, "message": 'Invalid JSON data'})