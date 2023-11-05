from django.urls import path
from . import views

app_name= 'shop'

urlpatterns = [
    path('', views.index, name="home"),
    path('products', views.Products.as_view(), name="products"),
    path('product/<pk>', views.Product_detail.as_view(), name="product_detail"),
    path('cart', views.cart, name="cart"),
    path('update_item', views.updateItem, name="update_item"),
    path('checkout', views.checkout, name="checkout")
]
