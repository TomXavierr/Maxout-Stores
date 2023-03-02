from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth import login, authenticate,logout
from customers.models import Account,Addresses

# from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


# Create your views here.

@login_required(login_url='user_login') 
def mens_store(request):
    products = Products.objects.filter(product_gender = 'Men')
    variants = Variants.objects.filter(variant_product__in = products )
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    count = variants.count()
    cart = Cart.objects.get(customer = request.user)
    cartitems = CartItem.objects.filter(cart= cart)
    total = cartitems.count
    context = {'products':products, 'count': count,'cart_count':total, 'variants': variants , 'sports':sports ,'brands':brands}
    
    return render(request,'store.html',context)


@login_required(login_url='user_login') 
def womens_store(request):
    products = Products.objects.filter(product_gender = 'Women')
    variants = Variants.objects.filter(variant_product__in = products )
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    count = variants.count()
    cart = Cart.objects.get(customer = request.user)
    cartitems = CartItem.objects.filter(cart= cart)
    total = cartitems.count
    context = {'products':products, 'count': count,'cart_count':total, 'variants': variants, 'sports':sports ,'brands':brands}
    
    return render(request,'store.html',context)

@login_required(login_url='user_login') 
def mensSport(request,id):
    products = Products.objects.filter(product_gender = 'Men', product_sport=id)
    variants = Variants.objects.filter(variant_product__in = products )
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    count = variants.count()
    cart = Cart.objects.get(customer = request.user)
    cartitems = CartItem.objects.filter(cart= cart)
    total = cartitems.count
    context = {'products':products, 'count': count,'cart_count':total, 'variants': variants, 'sports':sports ,'brands':brands}
    
    return render(request,'store.html',context)
@login_required(login_url='user_login') 
def womensSport(request,id):
    products = Products.objects.filter(product_gender = 'Women', product_sport=id)
    variants = Variants.objects.filter(variant_product__in = products )
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    count = variants.count()
    cart = Cart.objects.get(customer = request.user)
    cartitems = CartItem.objects.filter(cart= cart)
    total = cartitems.count
    context = {'products':products, 'count': count,'cart_count':total, 'variants': variants, 'sports':sports ,'brands':brands}
    
    return render(request,'store.html',context)


@login_required(login_url='user_login') 
def mensBrands(request,id):
    products = Products.objects.filter(product_gender = 'Men', product_brand=id)
    variants = Variants.objects.filter(variant_product__in = products )
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    count = variants.count()
    cart = Cart.objects.get(customer = request.user)
    cartitems = CartItem.objects.filter(cart= cart)
    total = cartitems.count
    context = {'products':products, 'count': count,'cart_count':total, 'variants': variants, 'sports':sports ,'brands':brands}

    return render(request,'store.html',context)

@login_required(login_url='user_login') 
def womensBrands(request,id):
    products = Products.objects.filter(product_gender = 'Women', product_brand=id)
    variants = Variants.objects.filter(variant_product__in = products )
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    count = variants.count()
    cart = Cart.objects.get(customer = request.user)
    cartitems = CartItem.objects.filter(cart= cart)
    total = cartitems.count
    context = {'products':products, 'count': count,'cart_count':total, 'variants': variants, 'sports':sports ,'brands':brands}

    return render(request,'store.html',context)


@login_required(login_url='user_login') 
def product_details(request,id): 
    details = Variants.objects.get(id=id)
    colour = details.variant_color
    product = Products.objects.get(id=details.variant_product.id)
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    cart = Cart.objects.get(customer = request.user)
    cartitems = CartItem.objects.filter(cart= cart)
    total = cartitems.count
    
    variants  = Variants.objects.filter(variant_product=product,variant_color=colour)
    sizes = Variants.objects.values_list('variant_size', flat=True).distinct()
    print(sizes)
    context = {'details':details , 'variants':variants,'cart_count':total ,'sizes':sizes, 'sports':sports ,'brands':brands }
    return render(request,'product_details.html',context)   


@login_required(login_url='user_login') 
def cart(request):
    customer  = request.user
    cart ,created =Cart.objects.get_or_create(customer=customer)
    cartitems = cart.cartitem_set.all()   
    context   = {'cartitems':cartitems,'cart':cart}
    return render(request,'cart.html',context)

def add_to_cart(request):
    if request.method == 'POST':
        user_cart, created = Cart.objects.get_or_create(customer=request.user)
        data = request.POST
        product_variant_id = data.get('product_variant_id')
        size = data.get('size')
        print("sdasdsa")
        product_variant = get_object_or_404(Variants, id=product_variant_id)
        stock = get_object_or_404(Variants, variant=product_variant, size=size)
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product_var=product_variant, size=size)
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
        return JsonResponse(response_data)
    
    
    
    
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
    address   = addresses.first()
    return render(request,'checkout.html',{'cart':cart,'cartitems':cartitems,'address':address})