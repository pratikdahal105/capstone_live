from rest_framework import serializers
from booking.models import Booking
from booking_verification.models import Booking_Verification
from event.models import Event
from datetime import timedelta
from django.utils import timezone
import secrets
from .mail import send_booking_email

class EventSlugField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return Event.objects.get(slug=data)
        except Event.DoesNotExist:
            raise serializers.ValidationError(f"Event with slug '{data}' does not exist.")

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name']
        
class BookingSerializer(serializers.ModelSerializer):
    event = EventSlugField(queryset=Event.objects.all(), slug_field='slug')
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    total = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Booking
        fields = ['event', 'quantity', 'total', 'status', 'user']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        event = validated_data['event']
        quantity = validated_data['quantity']

        total = quantity * event.price
        validated_data['total'] = total
        validated_data['user'] = user

        booking = Booking.objects.create(**validated_data)

        token = secrets.token_urlsafe(10)

        if booking.event.end_date:
            valid_till = booking.event.end_date
        else:
            valid_till = timezone.now() + timedelta(days=365)

        Booking_Verification.objects.create(
            booking=booking,
            token=token,
            valid_till=valid_till,
            status=0
        )

        send_booking_email(user, token)

        return booking

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        if 'quantity' in validated_data:
            instance.total = validated_data['quantity'] * instance.event.price
        else:
            instance.total = validated_data.get('total', instance.total)
        
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
