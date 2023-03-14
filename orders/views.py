from django.shortcuts import render, redirect
from store.models import *
from .models import *
from customers.models import *
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.


def place_cod_order(request):
    
    if request.method == 'POST':
        data           = request.POST
        address        = data.get('address_id')
        coupon_code    = data.get('coupon_code')
        payment_method = 'COD'
        print(address)
        print(coupon_code)
        
        order_id    = uuid.uuid4().hex[:8].upper()
        user        = request.user
        cart        = Cart.objects.get(customer=user)
        sub_total   = cart.cart_total
        cart_items  = CartItem.objects.filter(cart__customer=user)
        print(cart)
        print(cart_items)
        print(sub_total)
        
        
        if coupon_code:
            coupon = Coupons.objects.get(coupon_code=coupon_code)
            discount = coupon.discount_price
            grand_total = float(sub_total) - discount
        else:
            discount = 0
            grand_total = sub_total

        
        order =  Orders.objects.create(
            order_id          = order_id,
            user              = user,
            delivery_address  = Addresses.objects.get(id=address),
            order_total       = sub_total,
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
        
        request.session['order_id'] = order_id
        
        
        return JsonResponse  ({'success': True})
        # else:
        #     return redirect('order_success_page')
        
# @csrf_exempt
# def payment_verification(request):
    
#             try:
#                   payment_id = request.POST.get('razorpay_payment_id','')
#                   order_id = request.POST.get('razorpay_order_id','')
#                   signature = request.POST.get('razorpay_signature','')
#                   params_dict = {
#                         'razorpay_payment_id':payment_id ,
#                         'razorpay_order_id': order_id ,
#                         'razorpay_signature':signature
#                   }

#                   print(payment_id,'id')
#                   print(order_id,'order')
#                   print(signature,'signat')
#             except:
#                   pass
#             try:
#                 client.utility.verify_payment_signature(params_dict)
#             except:
#                   messages.info(request,'Payment Failed')
#                   print('failed')
#                   return redirect('checkout')
            
            
#             request.session['payment_id'] = payment_id
           
#             return redirect('placeorder')


def order_success_page(request):
    order       = Orders.objects.get(order_id=request.session['order_id'])
    order_items = order.orderitem_set.all()
    context = {
    'main_banner':  Banners.objects.get(id=1).banners,
    'cart_count':   CartItem.objects.filter(cart= Cart.objects.get(customer = request.user)).count(),
    'sports':       Sport.objects.all(),
    'brands':       Brand.objects.all() ,
    'user':         request.user,
    'Products':     Products,
    'order':        order ,
    'order_items':  order_items
    }
   
    
    print(order_items)
    
    return render(request,'order_succespage.html',context)

def order_details(request,id):
    
    order       = Orders.objects.get(id=id)
    order_items = order.orderitem_set.all()
    context = {
    'main_banner':  Banners.objects.get(id=1).banners,
    'cart_count':   CartItem.objects.filter(cart= Cart.objects.get(customer = request.user)).count(),
    'sports':       Sport.objects.all(),
    'brands':       Brand.objects.all() ,
    'user':         request.user,
    'Products':     Products,
    'order':        order ,
    'order_items':  order_items
    }
    return render(request,'order_details.html',context)

def cancel_order(request,id):
    order       = Orders.objects.get(id=id)   
    print(order)
    print(order.status)
    order.status = 'Cancelled'
    order.save()
    print(order.status)
    return redirect('my_orders')
