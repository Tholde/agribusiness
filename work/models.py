from django.db import models

from users.models import User


# Create your models here.
class Work(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technicien = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='works/')
    date = models.DateField(auto_now_add=True)


class Event(models.Model):
    title = models.CharField(max_length=200)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    class_name = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title