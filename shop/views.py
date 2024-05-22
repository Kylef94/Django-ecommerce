from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic
from django.http import JsonResponse
import json
from .models import *
from .forms import *


def index(request):
    return render(request, 'shop/index.html')

    
class Products(generic.ListView):
    model = Product
    template_name = 'shop/products.html'
    context_object_name = 'product_list'


class Product_detail(generic.DetailView):
    model = Product
    template_name = 'shop/product_detail.html'

    def get_queryset(self):
        return Product.objects.filter(pk=self.kwargs['pk'])

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        
    else:
        items = []
        order = {'get_total': 0, 'get_total_qty': 0}
    
    context = {'items': items, 'order': order}
    return render(request, 'shop/cart.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = int(data['productId'])
    action = data['action']
    
    print('action:', action)
    print('productid:', productId)
    
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderitem, created =  OrderItem.objects.get_or_create(order=order,product=product)
    
    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)
    
    if orderitem.quantity <= 0:
        orderitem.delete()
    else:
        orderitem.save()
        
    return JsonResponse('Item was added', safe=False)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        form = CheckoutForm()
        
    else:
        items = []
        order = {'get_total': 0, 'get_total_qty': 0}
        form = CheckoutForm()
    
    context = {'items': items, 'order': order, 'form': form}
    return render(request, 'shop/checkout.html', context)

class Checkout(generic.View):
    