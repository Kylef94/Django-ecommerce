from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic
from .models import Product
# Create your views here.

def index(request):
    return render(request, 'shop/index.html')

class Products(generic.ListView):
    model = Product
    template_name = 'shop/products.html'
    context_object_name = 'product_list'


class Product_detail(generic.DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(id=self.kwargs['pk'])
