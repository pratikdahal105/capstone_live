from django.db import models
from django.contrib.auth.models import User
from event.models import Event


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = "booking"