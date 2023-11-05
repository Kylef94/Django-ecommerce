from django.db import models
import uuid
from django.utils import timezone

from accounts.models import Customer


class Product(models.Model):
    name = models.CharField(max_length=30, null=False)
    price = models.FloatField()
    description = models.CharField(max_length=500)
    qty_in_stock = models.IntegerField(null=False)
    slug = models.SlugField()
    picture = models.ImageField(upload_to='media/product_pictures/', default='static/images/pic-not-found.jpg')
    date_added = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    

    def __str__(self):
        return f"Name: {self.name}"

class Category(models.Model):
    name = models.CharField(max_length=30, null=False)
    picture = models.ImageField(upload_to='media/category_pictures/', default='static/images/pic-not-found.jpg')
    products = models.ManyToManyField(Product)
    slug = models.SlugField()
    
    def __str__(self):
        return f"Name: {self.name}"
    

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    promo = models.CharField(max_length=30, null=False)
    start = models.DateField("Start Date", auto_now_add=True)
    end = models.DateField("End Date")
    amount = models.FloatField()
    
    def __str__(self) -> str:
        return f"Promo Name: {self.promo}\nProduct: {self.product.name}\nAmount: {self.amount}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank=False)
    txn_id = models.CharField(max_length=200, null=True)
    
    def __str__(self) -> str:
        return str(self.id)
    
    @property
    def get_total(self):
        items = self.orderitem_set.all()
        total = sum([item.get_item_total for item in items])
        return total
    
    @property
    def get_total_qty(self):
        items = self.orderitem_set.all()
        total = sum([item.quantity for item in items])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True)
    added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_item_total(self):
        total = self.product.price * self.quantity
        return total