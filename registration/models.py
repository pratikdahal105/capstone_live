from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.TextField(max_length=20, blank=True)
    status = models.PositiveSmallIntegerField(default=2, null=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.TextField(max_length=20, blank=True)
    status = models.PositiveSmallIntegerField(default=1)
    valid_till = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "token"