from django.db import models

from users.models import User


# Create your models here.
class Association(models.Model):
    logo = models.ImageField(upload_to='logo/', null=True, blank=True)
    name = models.CharField(max_length=100)
    technicien = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)


class Activity(models.Model):
    title = models.CharField(max_length=255)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='activity/', null=True, blank=True)
    description = models.TextField()
    budget = models.FloatField()


class MiniProject(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='miniproject/', null=True, blank=True)
    description = models.TextField()
    file = models.FileField(upload_to='miniproject/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    budget = models.FloatField()
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)


class Formation(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='formation/', null=True, blank=True)
    description = models.TextField()
    file = models.FileField(upload_to='formation/', null=True, blank=True)
    technicien = models.ForeignKey(User, on_delete=models.CASCADE, related_name='technicien', null=True, blank=True)
    # association = models.ForeignKey(Association, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Temoignage(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='temoignage/', null=True, blank=True)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)