from django.shortcuts import render, redirect
from store.models import *
from .models import *
from customers.models import *

# Create your views here.


def place_order(request):
    
    if request.method == 'POST':
        address        = request.POST['address']
        payment_method = request.POST['payment_method']
        print(address)
        print(payment_method)  
        
        user        = request.user
        cart        = Cart.objects.get(customer=user)
        cart_total  = cart.cart_total
        grand_total = cart_total
        cart_items  = CartItem.objects.filter(cart__customer=user)
        print(cart)
        print(cart_items)
        print(cart_total)
        
        if payment_method == 'COD':
            order =  Orders.objects.create(
                user              = user,
                delivery_address  = Addresses.objects.get(id=address),
                order_total       = cart_total,
                payment_method    = payment_method,
                grand_total       = grand_total,
                cart              = cart,          
            )
            order.save()
            
            for item in cart_items:
                orderitem = OrderItem.objects.create(
                    order      = order,
                    product    = item.product,
                    size       = item.size,
                    quantity   = item.product_qty,
                    price      = item.product.product_price,
                )
                orderitem.save()
            cart_items.delete()
        return render(request,'order_succespage.html')
        
def order_success(request):
   pass