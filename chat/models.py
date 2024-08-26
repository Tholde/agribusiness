from datetime import datetime

# from django.contrib.auth.models import User
from users.models import User
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=2000)
    date = models.DateTimeField(default=datetime.now)


class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)
