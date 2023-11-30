from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_1 = models.CharField("address line 1",max_length=50)
    address_2 = models.CharField("address line 2",max_length=50)
    address_3 = models.CharField("address line 3",max_length=50)
    city = models.CharField("city",max_length=50)
    postcode = models.CharField("postcode", max_length=10)
    country = CountryField()