from django.db import models
from event.models import Event

class Sponsor(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='images/uploads')
    description = models.TextField()
    amount_sponsored = models.DecimalField(max_digits=10, decimal_places=2)
    sponsor_level = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "sponsor"