from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=200)
    cover_picture = models.ImageField(upload_to='images/uploads')
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    available_seats = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.PositiveSmallIntegerField(blank=True, null=True)
    user = models.ManyToManyField(User, through='event_user')

    class Meta:
        db_table = "event"

class Event_User(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = "event_user"