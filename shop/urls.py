from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('products', views.Products.as_view(), name="products"),
    path('product/<int:pk>', views.Product_detail.as_view(), name="product_detail")
]
