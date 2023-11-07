from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from .managers import CustomerManager


class Customer(AbstractUser):
    """Customer user class which implements email rather than username default"""
    username = None
    email = models.EmailField("email address", unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomerManager()
    
    def __str__(self) -> str:
        return self.email
    
class Address(models.Model):
    """Registering customer address"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    line_1 = models.CharField(max_length=100)
    line_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    country = CountryField()
    postcode = models.CharField(max_length=10)
    date_added = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    
    
