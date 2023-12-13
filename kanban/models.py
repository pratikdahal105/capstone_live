from django.db import models
from django.contrib.auth.models import User


class Kanban(models.Model):
    slug = models.SlugField(unique=True)
    task = models.CharField(max_length=200)
    label = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    description = models.TextField()
    status = models.PositiveSmallIntegerField(blank=True, null=True)
    user = models.ManyToManyField(User, through='kanban_user')

    class Meta:
        db_table = "kanban"

class Kanban_User(models.Model):
    kanban = models.ForeignKey(Kanban, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "kanban_user"
