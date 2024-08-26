from django.utils import timezone

from django.db import models

from users.models import User


# Create your models here.
class Visitor(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now)


class UserProblem(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    problem = models.TextField()
    status = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
