from rest_framework.response import Response
from rest_framework.decorators import api_view
from booking.models import Booking
from event.models import Event, Event_User
from booking_verification.models import Booking_Verification
from .serializers import BookingSerializer
from api.user_api.decorators import require_authenticated_and_valid_token as valid_token
import qrcode
from io import BytesIO

@api_view(["GET"])
def test(request):
    data = {"status": True, "message": "Testing Booking API", "data": None}
    return Response(data, status=200)

@api_view(['GET', 'POST'])
@valid_token
def booking_list_create(request):
    if request.method == 'GET':
        user_profile_status = request.user.profile.status

        if user_profile_status == 0:
            bookings = Booking.objects.all()
        elif user_profile_status == 1:
            events = Event.objects.filter(user=request.user)
            bookings = Booking.objects.filter(event__in=events)
        elif user_profile_status == 2:
            bookings = Booking.objects.filter(user=request.user)
        else:
            bookings = Booking.objects.none()

        booking_data = []
        for booking in bookings:
            serialized_booking = BookingSerializer(booking).data

            try:
                booking_verification = Booking_Verification.objects.get(booking=booking)
                # qr_code_data = generate_qr_code_data(booking_verification.token)
                # serialized_booking['qr_code_data'] = qr_code_data
                serialized_booking['verification_token'] = booking_verification.token
            except Booking_Verification.DoesNotExist:
                # serialized_booking['qr_code_data'] = None
                serialized_booking['verification_token'] = None

            booking_data.append(serialized_booking)

        return Response({"status": True, "message": "Booking list retrieved.", "data": booking_data})

    elif request.method == 'POST':
        serializer = BookingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Booking created.", "data": serializer.data}, status=201)
        return Response({"status": False, "message": "Booking creation failed.", "data": serializer.errors}, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@valid_token
def booking_detail(request, id):
    try:
        booking = Booking.objects.get(id=id)
    except Booking.DoesNotExist:
        return Response({"status": False, "message": "Booking not found.", "data": None}, status=404)

    if request.user != booking.user:
        return Response({"status": False, "message": "Unauthorized access.", "data": None}, status=403)

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

@api_view(['POST'])
@valid_token
def update_booking_verification(request):
    if request.user.profile.status == 1:
        token = request.data.get('token', None)
        try:
            booking_verification = Booking_Verification.objects.get(token=token)
            event = booking_verification.booking.event
        except Booking_Verification.DoesNotExist:
            return Response({"status": False, "message": "Invalid token."}, status=404)

        if booking_verification.status == 1:
            return Response({"status": False, "message": "This ticket has already been verified."}, status=400)
        
        if request.user.profile.status != 1:
            if not Event_User.objects.filter(event=event, user=request.user).exists():
                return Response({"status": False, "message": "Unauthorized access. This is not your Event!"}, status=403)

        booking_verification.status = 1
        booking_verification.save()

        booking = booking_verification.booking
        event_title = booking.event.name
        quantity = booking.quantity
        total_cost = booking.total

        return Response({
            "status": True,
            "message": "Booking verification status updated.",
            "data": {
                "Event Title": event_title,
                "Booking Quantity": quantity,
                "Total Cost": total_cost
            }
        })
    else:
        return Response({"status": False, "message": "Unauthorized access."}, status=403)

