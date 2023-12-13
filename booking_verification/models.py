from django.db import models
from booking.models import Booking

class Booking_Verification(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    valid_till = models.DateTimeField()
    status = models.PositiveSmallIntegerField(blank=True, null=True)