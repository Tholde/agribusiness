from django.db import models

from users.models import User


# Create your models here.
class Product(models.Model):
    image = models.ImageField(upload_to='products/')
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    is_commanded = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    technicien = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    commanded_date = models.DateTimeField(null=True)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reference = models.CharField(max_length=255)
    is_accepted = models.BooleanField(default=False)
    date_envoyer = models.DateTimeField(auto_now_add=True)
    nom_de_compte = models.CharField(max_length=255)


class DemandLivraison(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    fees = models.FloatField()
    fournisseur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demandlivraisons_fournisseur')
    technicien = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demandlivraisons_technicien')
    is_accepted = models.BooleanField(default=False)
