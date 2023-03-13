from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth import login, authenticate,logout
from customers.models import Account,Addresses
from orders.models import Orders ,Coupons   
from django.views.decorators.http import require_POST

# from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from django.contrib import messages
from customers.views import check_user

import re

# Create your views here.

@login_required(login_url='user_login') 
@check_user
def mens_store(request):
    
    products     = Products.objects.filter(product_gender = 'Men')
    variants     = Variants.objects.filter(variant_product__in = products )
    count = products.count()
    sports       =  Sport.objects.all()
    brands       = Brand.objects.all()
    
    cart      = Cart.objects.get(customer = request.user)
    cartitems = CartItem.objects.filter(cart= cart)
    total     = cartitems.count
    context   = {'products':products,'count': count, 'variants': variants , 'cart_count':total, 'sports':sports ,'brands':brands  }
    
    return render(request,'store.html',context)


@login_required(login_url='user_login') 
@check_user
def womens_store(request):
    products = Products.objects.filter(product_gender = 'Women')
    variants = Variants.objects.filter(variant_product__in = products )
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    count = products.count()
    cart = Cart.objects.get(customer = request.user)
    cartitems = CartItem.objects.filter(cart= cart)
    total = cartitems.count
    context = {'products':products, 'count': count,'cart_count':total, 'variants': variants, 'sports':sports ,'brands':brands}
    
    return render(request,'store.html',context)

@login_required(login_url='user_login') 
@check_user
def mensSport(request,id):
    products = Products.objects.filter(product_gender = 'Men', product_sport=id)
    variants = Variants.objects.filter(variant_product__in = products )
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    count = products.count()
    cart = Cart.objects.get(customer = request.user)
    cartitems = CartItem.objects.filter(cart= cart)
    total = cartitems.count
    context = {'products':products, 'count': count,'cart_count':total, 'variants': variants, 'sports':sports ,'brands':brands}
    
    return render(request,'store.html',context)

@login_required(login_url='user_login') 
@check_user
def womensSport(request,id):
    products = Products.objects.filter(product_gender = 'Women', product_sport=id)
    variants = Variants.objects.filter(variant_product__in = products )
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    count = products.count()
    cart = Cart.objects.get(customer = request.user)
    cartitems = CartItem.objects.filter(cart= cart)
    total = cartitems.count
    context = {'products':products, 'count': count,'cart_count':total, 'variants': variants, 'sports':sports ,'brands':brands}
    
    return render(request,'store.html',context)


@login_required(login_url='user_login') 
@check_user
def mensBrands(request,id):
    products = Products.objects.filter(product_gender = 'Men', product_brand=id)
    variants = Variants.objects.filter(variant_product__in = products )
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    count = products.count()
    cart = Cart.objects.get(customer = request.user)
    cartitems = CartItem.objects.filter(cart= cart)
    total = cartitems.count
    context = {'products':products, 'count': count,'cart_count':total, 'variants': variants, 'sports':sports ,'brands':brands}

    return render(request,'store.html',context)

@login_required(login_url='user_login') 
@check_user
def womensBrands(request,id):
    products = Products.objects.filter(product_gender = 'Women', product_brand=id)
    variants = Variants.objects.filter(variant_product__in = products )
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    count = products.count()
    cart = Cart.objects.get(customer = request.user)
    cartitems = CartItem.objects.filter(cart= cart)
    total = cartitems.count
    context = {'products':products, 'count': count,'cart_count':total, 'variants': variants, 'sports':sports ,'brands':brands}

    return render(request,'store.html',context)


@login_required(login_url='user_login') 
def product_details(request,id): 
    details = Products.objects.get(id=id)
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    cart = Cart.objects.get(customer = request.user)
    cartitems = CartItem.objects.filter(cart= cart)
    total = cartitems.count
    
    variants  = Variants.objects.filter(variant_product=details.id).order_by('-variant_size')
   
    
    context = {'details':details , 'variants':variants,'cart_count':total ,'sports':sports ,'brands':brands }
    return render(request,'product_details.html',context)   


@login_required(login_url='user_login') 
def cart(request):
    customer  = request.user
    cart      = Cart.objects.get(customer=customer)
    cartitems = cart.cartitem_set.all() 
    print(cartitems)  
    count     = cartitems.count
    
    
    context   = {'cartitems':cartitems,'cart':cart, 'cart_count':count}
    return render(request,'cart.html',context)




def add_to_cart(request):
    if request.method == 'POST':
        user_cart     = Cart.objects.get(customer=request.user)
        print(user_cart)
        data          = request.POST
        product_id    = data.get('product_id')
        product       = Products.objects.get(id=product_id)
        size_id       = data.get('size')
        size          = Size.objects.get(id=size_id)
        print(size)
        print(product_id)
        variant         = Variants.objects.get(variant_product=product_id,variant_size=size.id)
       
        print(variant)
     
        print(variant.variant_stock)
        
        if(variant.variant_stock >0):
            cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product, size=size.size)
            if not created:
                cart_item.product_qty += 1
                cart_item.save()
            else:
                cart_item.product_qty = 1
                cart_item.save()
            response_data = {
                'success': True,
                'message': 'Item added to cart.',
                'cart_item_count': user_cart.cartitem_set.count()
            }
        else:
            response_data = {
                'success': False,
                'message': 'Item out of Stock.',
            }
        return JsonResponse(response_data)
    
def update_cart_quantity(request):
   
  if request.method == 'POST':
    email = request.user
   # print(email)
    data          = request.POST
    total        = 0
    cartitems    = 0
    item_id      = data.get('item_id')
   # print(item_id)
    cart_item    = CartItem.objects.get(id=item_id)
   # print(cart_item)
    quantity     = data.get('quantity')
    cart_item    = CartItem.objects.get(id=item_id)
    cart         = Cart.objects.filter(customer = request.user)
    
    
    product_id   = cart_item.product.id
    size       = cart_item.size
    size_obj    = Size.objects.get(size=size)
    #print(size)
    variant = Variants.objects.get(variant_product=product_id,variant_size=size_obj.id)
    stock = variant.variant_stock

    if stock < int(quantity):
        print('error message')
        response_data = {
            'success': False,'status': 'error', 'message': 'sorry only  '+ str(stock) + '  pieces in stock'
            }
        return JsonResponse({'status': 'error', 'message': 'sorry only  '+ str(stock) + '  pieces in stock'})
    
    cart_item.product_qty = quantity
    cart_item.save()
    print( 'qty after'+str(cart_item.product_qty))
    print('jbbmnb')
    Sub_total = int(cart_item.product.product_price)*int(cart_item.product_qty)
    print(Sub_total)
    
    
    
    cart_items = CartItem.objects.filter(cart__customer__email = email )
    print(cart_items)
    
    for items in cart_items:
        total += items.product_qty * items.product.product_price
        cartitems += items.product_qty
    print(total)
    print(cartitems)
    
    # grand_total = (total+tax)
   
    return JsonResponse({
      'quantity': quantity,
      'total': total,
      'cartitems':cartitems,
    #   'grand_total':grand_total, 
      'Sub_total':Sub_total,
    })
  else:
    return JsonResponse({})


    
    
def delete_cartitem(request,id):
    
    item =CartItem.objects.get(id=id)
    item.delete()
    return redirect('cart')


def updatecart(request):
    return JsonResponse('Item was added',safe=False)

def checkout(request):
    cart      = Cart.objects.get(customer=request.user)
    cartitems = CartItem.objects.filter(cart=cart)
    user      = request.user
    addresses = Addresses.objects.filter(user_id=user)
   
    grand_total = 0
    for items in cartitems:
        grand_total += items.product_qty * items.product.product_price
    print(grand_total)
    
    return render(request,'checkout.html',{'cart':cart,'cartitems':cartitems,'addresses':addresses, 'Orders':Orders ,'grand_total':grand_total})
@require_POST
def redeem_coupon(request):
    code = request.POST.get('code')
    try:
        coupon = Coupons.objects.get(code=code)
        request.session['coupon_id'] = coupon.id
        return JsonResponse({'success': True})
    except Coupons.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid coupon code'})

def add_checkout_address(request):
    user = request.user
    user_id = user.id
    print(user_id)
    
    if request.method == 'POST':
        first_name     = request.POST['first_name']
        last_name      = request.POST['last_name']
        house_name     = request.POST['house_name']
        street_name    = request.POST['street_name']
        city           = request.POST['city']
        district       = request.POST['district']
        state          = request.POST['state']
        pincode        = request.POST['pincode']
        mobile         = request.POST['mobile']
        
        if first_name and last_name and house_name and street_name and city and district and state and pincode and mobile :
            if not re.match(r'^\d{10}$', mobile):
                # email is invalid
                error_message = "Please enter a valid Mobile number."
                return render(request, 'checkoutaddress.html', {'error_message': error_message})
            
            else:
                if Addresses.objects.filter(user_id=user_id):
                    address = Addresses.objects.create(
                        first_name   = first_name,
                        last_name    = last_name,
                        house_name   = house_name,
                        street_name  = street_name,
                        city         = city,
                        district     = district,
                        state        = state,
                        pincode      = pincode,
                        mobile       = mobile,
                        user_id      = Account.objects.get(id=user_id)
                    )
                else:
                    address = Addresses.objects.create(
                        first_name   = first_name,
                        last_name    = last_name,
                        house_name   = house_name,
                        street_name  = street_name,
                        city         = city,
                        district     = district,
                        state        = state,
                        pincode      = pincode,
                        mobile       = mobile,
                        user_id      = Account.objects.get(id=user_id),
                        is_primary   = True,
                    )
            return redirect('checkout')
        else:
            messages.info(request,'Input all fields')
            return redirect('add_checkout_address')
    else:
        return render(request, 'checkoutaddress.html')
    
    
def delete_address2(request,id):
    address = Addresses.objects.get(id=id)
    address.delete()
    return redirect('checkout')
    
    
def search_products(request):
    if request.method=='GET':
        searchterm =request.GET.get('searchterm')
        print(searchterm)
        products=Products.objects.filter(product_name__icontains = searchterm)
        return render(request,'store.html',{'products':products})
    