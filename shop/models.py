from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField()
    description = models.CharField(max_length=500)
    qty_in_stock = models.IntegerField()
    picture = models.ImageField(upload_to='media/product_pictures/', default='static/images/pic-not-found.jpg')

    def __str__(self):
        return self.name
        
class cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.one
    