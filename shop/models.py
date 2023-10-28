from django.db import models
import uuid
from django.utils import timezone

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=30, null=False)
    ref_code = models.UUIDField(default=uuid.uuid4, editable=False)
    price = models.FloatField()
    description = models.CharField(max_length=500)
    qty_in_stock = models.IntegerField(null=False)
    slug = models.SlugField()
    picture = models.ImageField(upload_to='media/product_pictures/', default='static/images/pic-not-found.jpg')
    date_added = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    

    def __str__(self):
        return f"Name: {self.name}\nref code: {self.ref_code}"

class Category(models.Model):
    name = models.CharField(max_length=30, null=False)
    ref_code = models.UUIDField(default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to='media/category_pictures/', default='static/images/pic-not-found.jpg')
    products = models.ManyToManyField(Product)
    slug = models.SlugField()
    
    def __str__(self):
        return f"Name: {self.name}\n ref code: {self.ref_code}"
    

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    promo = models.CharField(max_length=30, null=False)
    ref_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start = models.DateField("Start Date", auto_now_add=True)
    end = models.DateField("End Date")
    amount = models.FloatField()
    
    def __str__(self) -> str:
        return f"Promo Name: {self.promo}\nProduct: {self.product.name}\nAmount: {self.amount}"
    