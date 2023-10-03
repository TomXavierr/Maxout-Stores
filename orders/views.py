from django.shortcuts import render, redirect
from store.models import *
from .models import *
from customers.models import *
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import razorpay
from django.contrib import messages
from django.conf import settings
from django.views.decorators.cache import never_cache
# Create your views here.

@never_cache
def place_cod_order(request):  # sourcery skip: last-if-guard
    
    if request.method == 'POST':
        data           = request.POST
        address        = data.get('address_id')
        coupon_code = request.session.get('coupon_code')
        payment_method = 'COD'
        
        order_id    = uuid.uuid4().hex[:8].upper()
        user        = request.user
        cart        = Cart.objects.get(customer=user)
        sub_total   = cart.cart_total
        cart_items  = CartItem.objects.filter(cart__customer=user)
        if coupon_code:
            coupon = Coupons.objects.get(coupon_code=coupon_code)
            discount = coupon.discount_price
            grand_total = float(sub_total) - discount
            del request.session['coupon_code']
        else:
            discount = 0
            grand_total = sub_total

        
        order =  Orders.objects.create(
            order_id          = order_id,
            user              = user,
            discount_given    = discount,
            delivery_address  = Addresses.objects.get(id=address),
            order_total       = sub_total,
            payment_method    = payment_method,
            grand_total       = grand_total,
            cart              = cart,          
        )
        order.save()
        
        #saves the payment information 
        payment = Payment.objects.create(user = request.user, payment_method=payment_method,status='NOT PAID',amount_paid ='0',order=order )
        payment.save()
        
        for item in cart_items:
            size      = item.size
            size_id   = Size.objects.get(size=size)
            quantity  = item.product_qty
            product   = item.product
            variant   = Variants.objects.get(variant_product=product,variant_size=size_id)
            variant.variant_stock -= int(quantity)
            variant.save()
        
        
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

@never_cache 
def review_order(request):
     if request.method == 'POST':
        data           = request.POST
        address        = data.get('address_id')
        print(address)
        request.session['address'] = address
  
        return JsonResponse  ({'success': True})
     

@never_cache   
def payment(request):
    coupon_code = request.session.get('coupon_code')
    address_id     = request.session.get('address')

    address    = Addresses.objects.get(id=address_id)
    user       = request.user
    cart       = Cart.objects.get(customer = user)
    sub_total   = cart.cart_total
    cart_items  = CartItem.objects.filter(cart__customer=user)
        
    if coupon_code:
        coupon = Coupons.objects.get(coupon_code=coupon_code)
        discount = coupon.discount_price
        grand_total = float(sub_total) - discount
    else:
        discount = 0
        grand_total = sub_total

    amount_in_paisa = int(grand_total)*100
    client = razorpay.Client(auth = (settings.KEY,settings.SECRET))

    order_data = {
    'amount': amount_in_paisa,
    'currency': 'INR',
      }

    payment = client.order.create(data=order_data)

    return render(request, 'review_order.html',locals())
   
@csrf_exempt
def payment_verification(request):
    
            try:
                  payment_id = request.POST.get('razorpay_payment_id','')
                  order_id = request.POST.get('razorpay_order_id','')
                  signature = request.POST.get('razorpay_signature','')
                  
                  params_dict = {
                        'razorpay_payment_id':payment_id ,
                        'razorpay_order_id': order_id ,
                        'razorpay_signature':signature
                  }

            except:
                  pass
              
            try:
                client = razorpay.Client(auth = (settings.KEY,settings.SECRET))
                client.utility.verify_payment_signature(params_dict)
            except:
                  messages.info(request,'Payment Failed')
                  print('failed')
                  
            
            request.session['payment_id'] = payment_id
            return redirect('payment_success')
        
@never_cache
def payment_success(request):
    coupon_code = request.session.get('coupon_code')
    address_id     = request.session.get('address')
    payment_method = 'Razorpay'
    print(coupon_code)
    
    order_id    = uuid.uuid4().hex[:8].upper()
    user        = request.user
    cart        = Cart.objects.get(customer=user)
    sub_total   = cart.cart_total
    cart_items  = CartItem.objects.filter(cart__customer=user)
    
    if coupon_code:
        coupon = Coupons.objects.get(coupon_code=coupon_code)
        discount = coupon.discount_price
        grand_total = float(sub_total) - discount
        del request.session['coupon_code']
    else:
        discount = 0
        grand_total = sub_total

    
    order =  Orders.objects.create(
        order_id          = order_id,
        user              = user,
        delivery_address  = Addresses.objects.get(id=address_id),
        order_total       = sub_total,
        payment_method    = payment_method,
        discount_given    = discount,
        grand_total       = grand_total,
        cart              = cart,          
    )
    order.save()
    
    #checks for the payment id in the session and creates payment information data
    if 'payment_id'  in request.session:
          payment_id = request.session['payment_id']
          payment = Payment.objects.create(user = request.user,payment_id=payment_id, payment_method=payment_method,status='Paid',amount_paid =grand_total,order=order )
          payment.save()
          del request.session['payment_id'] 
    
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
    return redirect('order_success_page')


def order_success_page(request):
    order       = Orders.objects.get(order_id=request.session['order_id'])
    order_items = order.orderitem_set.all()
    context = {
    'sports':       Sport.objects.all(),
    'brands':       Brand.objects.all() ,
    'user':         request.user,
    'Products':     Products,
    'order' :       order ,
    'order_items':  order_items
    }
   
    
    print(order_items)
    
    return render(request,'order_succespage.html',context)


def cancel_order(request,id):
    order       = Orders.objects.get(id=id)   
    order.status = 'Cancelled'
    order.save()
    return redirect('my_orders')
