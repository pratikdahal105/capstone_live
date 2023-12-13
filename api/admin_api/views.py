from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .serializers import UserWithProfileSerializer, EventSerializer, BookingSerializer
from api.user_api.decorators import require_authenticated_and_valid_token as valid_token
from .decorators import check_admin_status
from event.models import Event
from booking.models import Booking


@api_view(["GET"])
def test(request):
    data = {"status": True, "message": "Testing admin API", "data": None}
    return Response(data)

@api_view(['GET', 'POST'])
@valid_token
@check_admin_status
def user_list_create(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserWithProfileSerializer(users, many=True)
        return Response({"status": True, "message": "Users retrieved.", "data": serializer.data})

    elif request.method == 'POST':
        serializer = UserWithProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "New user created.", "data": serializer.data})
        return Response({"status": False, "message": "User creation failed.", "data": serializer.errors}, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@valid_token
@check_admin_status
def user_detail(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"status": False, "message": "User not found.", "data": None}, status=404)

    if request.method == 'GET':
        serializer = UserWithProfileSerializer(user)
        return Response({"status": True, "message": "User retrieved.", "data": serializer.data})

    elif request.method == 'PUT':
        serializer = UserWithProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "User updated.", "data": serializer.data})
        return Response({"status": False, "message": "User update failed.", "data": serializer.errors}, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return Response({"status": True, "message": "User deleted.", "data": None}, status=204)

@api_view(['GET', 'POST'])
@valid_token
@check_admin_status
def event_list_create(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response({"status": True, "message": "Events retrieved.", "data": serializer.data})

    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "New event created.", "data": serializer.data})
        return Response({"status": False, "message": "Event creation failed.", "data": serializer.errors}, status=400)
    
@api_view(['GET', 'PUT', 'DELETE'])
@valid_token
@check_admin_status
def event_detail(request, id):
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response({"status": False, "message": "Event not found.", "data": None}, status=404)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response({"status": True, "message": "Event retrieved.", "data": serializer.data})

    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Event updated.", "data": serializer.data})
        return Response({"status": False, "message": "Event update failed.", "data": serializer.errors}, status=400)

    elif request.method == 'DELETE':
        event.delete()
        return Response({"status": True, "message": "Event deleted.", "data": None}, status=204)

@api_view(['GET', 'POST'])
@valid_token
@check_admin_status
def booking_list_create(request):
    if request.method == 'GET':
        bookings = Booking.objects.select_related('event').all()
        serializer = BookingSerializer(bookings, many=True)
        return Response({"status": True, "message": "Bookings retrieved.", "data": serializer.data})

    elif request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "New booking created.", "data": serializer.data})
        return Response({"status": False, "message": "Booking creation failed.", "data": serializer.errors}, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@valid_token
@check_admin_status
def booking_detail(request, id):
    try:
        booking = Booking.objects.get(id=id)
    except Booking.DoesNotExist:
        return Response({"status": False, "message": "Booking not found.", "data": None}, status=404)

    if request.method == 'GET':
        serializer = BookingSerializer(booking)
        return Response({"status": True, "message": "Booking retrieved.", "data": serializer.data})

    elif request.method == 'PUT':
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Booking updated.", "data": serializer.data})
        return Response({"status": False, "message": "Booking update failed.", "data": serializer.errors}, status=400)

    elif request.method == 'DELETE':
        booking.delete()
        return Response({"status": True, "message": "Booking deleted.", "data": None}, status=204)
