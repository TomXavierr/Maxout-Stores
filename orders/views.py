from django.shortcuts import render
from store.models import *
from customers.models import *

# Create your views here.


def place_order(request):
    user        = request.user
    cart        = Cart.objects.get(customer=user)

    cart_items  = CartItem.objects.filter(cart__customer=user)
    print(cart)
    print(cart_items)
    # if request.method == 'POST':
    #     user        = request.user
    #     cart        = Cart.objects.get(customer=user)
    
    #     cart_items  = CartItem.objects.filter(cart__customer=user)
    #     print(cart)
    #     print(cart_items)
    
    