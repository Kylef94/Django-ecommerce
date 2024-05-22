from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_countries.fields import CountryField

User = get_user_model()

class Address(models.Model):
    ADDRESS_CHOICES = (
        ('B', 'Billing'),
        ('S', 'Shipping'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_2 = models.CharField("address line 2",max_length=50)
    address_1 = models.CharField("address line 1",max_length=50)
    city = models.CharField("city",max_length=50)
    postcode = models.CharField("postcode", max_length=10)
    country = CountryField()
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    
class Product(models.Model):
    name = models.CharField("product name",max_length=30)
    price = models.FloatField("product price" )
    description = models.CharField("product description",max_length=500)
    qty_in_stock = models.IntegerField("quantity in stock")
    picture = models.ImageField("product picture", upload_to='media/product_pictures/', default='static/images/pic-not-found.jpg')
    date_added = models.DateField("date added", auto_now_add=True)
    last_updated = models.DateField("last update date", auto_now=True)
    
    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        
    def __str__(self):
        return f"Product name: {self.name}"
    
    def get_absolute_url(self):
        return reverse("product_detail", args=[str(self.id)]) 
    
class Category(models.Model):
    name = models.CharField("category name", max_length=30, null=False)
    picture = models.ImageField("category picture",upload_to='media/category_pictures/', default='static/images/pic-not-found.jpg')
    products = models.ManyToManyField(Product)
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        
    def __str__(self):
        return f"Name: {self.name}"
    

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    promo = models.CharField("promotion name",max_length=30, null=False)
    start = models.DateField("Start Date", auto_now_add=True)
    end = models.DateField("End Date")
    amount = models.FloatField("discount amount")
    
    class Meta:
        verbose_name = "product discount"
        verbose_name_plural = "product discounts"
        
    def __str__(self) -> str:
        return f"Promo Name: {self.promo}\nProduct: {self.product.name}\nAmount: {self.amount}"

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField("date created",auto_now_add=True)
    complete = models.BooleanField("completed",default=False, blank=False)
    txn_id = models.CharField("transaction id", max_length=200, null=True)
    
    def __str__(self) -> str:
        return str(self.id)
    
    class Meta:
        verbose_name = "customer order"
        verbose_name_plural = "customer orders"
        
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField("order quantity", default=1)
    added = models.DateTimeField("date added", auto_now_add=True)
    
    billing_address = models.ForeignKey(
        Address, related_name='billing_address', blank=True, null=True, on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', blank=True, null=True, on_delete=models.SET_NULL)
    
    class Meta:
        verbose_name = "order item"
        verbose_name_plural = "order items"

    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"ORDER-{self.pk}"
    
        
    @property
    def get_item_total(self):
        total = self.product.price * self.quantity
        return total


