from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
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
import razorpay
import re
import json
from django.urls import reverse
from django.core.paginator import Paginator

# Create your views here.



# def shop(request):
    
#     products     = Products.objects.all()
#     variants     = Variants.objects.filter(variant_product__in = products )
#     count = products.count()
#     sports       =  Sport.objects.all()
#     brands       = Brand.objects.all()
#     if request.user.is_authenticated:
#         cart      = Cart.objects.get(customer = request.user)
#         cartitems = CartItem.objects.filter(cart= cart)
#         cart_count     = cartitems.count
    
#     return render(request,'store.html',locals())

def shop(request):
    search_term = request.GET.get('search_term')
    print("sdgshfhdfh")
    print(search_term)
    
    if search_term:
        products = Products.objects.filter(product_name__icontains=search_term)
    else:
        products = Products.objects.all()
    print(products)
    variants = Variants.objects.filter(variant_product__in=products)
    count = products.count()
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    if request.user.is_authenticated:
        cart = Cart.objects.get(customer=request.user)
        cartitems = CartItem.objects.filter(cart=cart)
        cart_count = cartitems.count
    
    items_per_page = 12
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)    
        
    
    return render(request, 'store.html', {
        'products': page_products,
        'variants': variants,
        'count': count,
        'sports': sports,
        'brands': brands,
        'cart_count': cart_count if request.user.is_authenticated else None,
    })

def mens_store(request):
    
    products     = Products.objects.filter(product_gender = 'Men')
    variants     = Variants.objects.filter(variant_product__in = products )
    count        = products.count()
    sports       =  Sport.objects.all()
    brands       = Brand.objects.all()
    gender       = "Men"
    
    
    if request.user.is_authenticated:
        cart      = Cart.objects.get(customer = request.user)
        cartitems = CartItem.objects.filter(cart= cart)
        cart_count     = cartitems.count
    
    items_per_page = 12
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number) 
    
    products = page_products
    return render(request,'store.html',locals())


def womens_store(request):
    products  = Products.objects.filter(product_gender = 'Women')
    variants  = Variants.objects.filter(variant_product__in = products )
    sports    = Sport.objects.all()
    brands    = Brand.objects.all()
    count     = products.count()
    gender    = "Women"
    
    if request.user.is_authenticated:
        cart      = Cart.objects.get(customer = request.user)
        cartitems = CartItem.objects.filter(cart= cart)
        cart_count     = cartitems.count
    
    items_per_page = 12
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number) 
    
    products = page_products
    
    return render(request,'store.html',locals())


def all_sport(request,id):
    products    = Products.objects.filter(product_sport=id)
    variants    = Variants.objects.filter(variant_product__in = products )
    sports      = Sport.objects.all()
    brands      = Brand.objects.all()
    count       = products.count()
    sport_id    = id
    
    if request.user.is_authenticated:
        cart      = Cart.objects.get(customer = request.user)
        cartitems = CartItem.objects.filter(cart= cart)
        cart_count     = cartitems.count
    
    items_per_page = 12
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number) 
    
    products = page_products
    
    return render(request,'store.html',locals())


def mensSport(request,id):
    products = Products.objects.filter(product_gender = 'Men', product_sport=id)
    variants = Variants.objects.filter(variant_product__in = products )
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    count = products.count()
    gender       = "Men"
    sport_id    = id
    
    
    if request.user.is_authenticated:
        cart      = Cart.objects.get(customer = request.user)
        cartitems = CartItem.objects.filter(cart= cart)
        cart_count     = cartitems.count

    items_per_page = 12
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number) 
    
    products = page_products
    
    return render(request,'store.html',locals())


def womensSport(request,id):
    products = Products.objects.filter(product_gender = 'Women', product_sport=id)
    variants = Variants.objects.filter(variant_product__in = products )
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    count = products.count()
    gender       = "Women"
    sport_id    = id
    
    if request.user.is_authenticated:
        cart      = Cart.objects.get(customer = request.user)
        cartitems = CartItem.objects.filter(cart= cart)
        cart_count     = cartitems.count
    
    items_per_page = 12
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number) 
    
    products = page_products
    
    return render(request,'store.html',locals())


def all_brands(request,id):
    products   = Products.objects.filter(product_brand=id)
    variants   = Variants.objects.filter(variant_product__in = products )
    sports     = Sport.objects.all()
    brands     = Brand.objects.all()
    count      = products.count()
    brand_id   = id
    
    if request.user.is_authenticated:
        cart      = Cart.objects.get(customer = request.user)
        cartitems = CartItem.objects.filter(cart= cart)
        cart_count     = cartitems.count
     
    items_per_page = 12
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number) 
    
    products = page_products
       
    return render(request,'store.html',locals())

 
def mensBrands(request,id):
    products        = Products.objects.filter(product_gender = 'Men', product_brand=id)
    variants        = Variants.objects.filter(variant_product__in = products )
    sports          = Sport.objects.all()
    brands          = Brand.objects.all()
    count           = products.count()
    gender          = "Men"
    brand_id        = id
    
    
    if request.user.is_authenticated:
        cart      = Cart.objects.get(customer = request.user)
        cartitems = CartItem.objects.filter(cart= cart)
        cart_count     = cartitems.count    
    
    items_per_page = 12
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number) 
    
    products = page_products
    
    return render(request,'store.html',locals())


def womensBrands(request,id):
    products     = Products.objects.filter(product_gender = 'Women', product_brand=id)
    variants     = Variants.objects.filter(variant_product__in = products )
    sports       = Sport.objects.all()
    brands       = Brand.objects.all()
    count        = products.count()
    
    gender       = "Women"
    brand_id     = id
    
    if request.user.is_authenticated:
        cart      = Cart.objects.get(customer = request.user)
        cartitems = CartItem.objects.filter(cart= cart)
        cart_count     = cartitems.count
    
    items_per_page = 12
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number) 
    
    products = page_products
    
    return render(request,'store.html',locals())


def ListByCategory(request,id):
    category    = Category.objects.get(id=id)
    products    = Products.objects.filter(product_category=category)
    variants    = Variants.objects.filter(variant_product__in = products )
    sports      = Sport.objects.all()
    brands      = Brand.objects.all()
    count       = products.count()
    
    category_id = id
    
    
    if request.user.is_authenticated:
        cart      = Cart.objects.get(customer = request.user)
        cartitems = CartItem.objects.filter(cart= cart)
        cart_count     = cartitems.count
    
    items_per_page = 12
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number) 
    
    products = page_products
    
    return render(request,'store.html',locals())


def ListByBrand(request,id):
    brand      = Brand.objects.get(id=id)
    products   = Products.objects.filter(product_brand=brand)
    brand_id   = id
    variants   = Variants.objects.filter(variant_product__in = products )
    sports     = Sport.objects.all()
    brands     = Brand.objects.all()
    count      = products.count()
    
  
    
    if request.user.is_authenticated:
        cart      = Cart.objects.get(customer = request.user)
        cartitems = CartItem.objects.filter(cart= cart)
        cart_count     = cartitems.count
    
    items_per_page = 12
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number) 
    
    products = page_products
    
    return render(request,'store.html',locals())



def product_details(request,id): 
    details = Products.objects.get(id=id)
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    variants  = Variants.objects.filter(variant_product=details.id).order_by('-variant_size')
    variants_json = json.dumps(list(variants.values()))
    
    
    if request.user.is_authenticated:
        cart            = Cart.objects.get(customer = request.user)
        cartitems       = CartItem.objects.filter(cart= cart)
        cart_count      = cartitems.count
        wishlist        = Wishlist.objects.get(user=request.user)
        wishlist_items  = WishlistItems.objects.filter(wishlist=wishlist, product=details)
        if wishlist_items.exists():
            in_wishlist = True
        else:
            in_wishlist = False
            
        
    
    return render(request,'product_details.html',locals())   


@login_required(login_url='user_login') 
def cart(request):
    customer  = request.user
    cart      = Cart.objects.get(customer=customer)
    cartitems = cart.cartitem_set.all() 
    print(cartitems)  
    count     = cartitems.count
    
    
    context   = {'cartitems':cartitems,'cart':cart, 'cart_count':count}
    return render(request,'cart.html',context)

@login_required(login_url='user_login') 
def add_to_cart(request):
    if request.method == 'POST':
        user_cart     = Cart.objects.get(customer=request.user)
        print(user_cart)
        data          = request.POST
        product_id    = data.get('product_id')
        data_quantity = data.get('quantity')
        quantity      = int(data_quantity)
        product       = Products.objects.get(id=product_id)
        size_id       = data.get('size')
        size          = Size.objects.get(id=size_id)
        print(size)
        print(product_id)
        print(quantity)
        variant         = Variants.objects.get(variant_product=product_id,variant_size=size.id)
       
        print(variant)
        print(variant.variant_stock)
        
        if CartItem.objects.filter(cart=user_cart,product=product,size=size.size).exists():
            cart_item     = CartItem.objects.get(cart=user_cart,product=product,size=size.size)
            item_quantity = cart_item.product_qty
            if quantity <= variant.variant_stock - item_quantity:
                cart_item.product_qty += quantity
                cart_item.save()
                print(cart_item.product_qty)
                response_data = {
                    'success': True,
                    'message': 'Item added to cart.',
                    'cart_item_count': user_cart.cartitem_set.count()
                }
            else:
                response_data = {
                'success': False,
                'message': 'Not enough stock.',
            }
                
        else:
            if quantity <= variant.variant_stock:
                cart_item = CartItem.objects.create(cart=user_cart, product=product, size=size.size,product_qty=int(quantity))
                response_data = {
                    'success': True,
                    'message': 'Item added to cart.',
                    'cart_item_count': user_cart.cartitem_set.count()
                }
            else:
                response_data = {
                    'success': False,
                    'message': 'Not enough stock.',
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

    if int(quantity) > 10:
        print('error message')
        response_data = {
            'success': False,'status': 'error', 'message': 'maximum units reached'
            }
        return JsonResponse({'status': 'error', 'message': 'maximum units reached'})
    else:
        if stock < int(quantity):
            print('error message')
            response_data = {
                'success': False,'status': 'error', 'message': 'sorry only  '+ str(stock) + '  pieces in stock'
                }
            return JsonResponse({'status': 'error', 'message': 'sorry only  '+ str(stock) + '  pieces in stock'})
        
        
        cart_item.product_qty = quantity
        cart_item.save()
        
        Sub_total = int(cart_item.product.product_price)*int(cart_item.product_qty)
        print(Sub_total)
            
        cart_items = CartItem.objects.filter(cart__customer__email = email )
        
        for items in cart_items:
            total += items.product_qty * items.product.product_price
            cartitems += items.product_qty
    
        
    
        return JsonResponse({
        'quantity': quantity,
        'total': total,
        'cartitems':cartitems,
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


@login_required(login_url='user_login') 
def wishlist(request):
    wishlist      = Wishlist.objects.get(user=request.user)
    wishlist_items = WishlistItems.objects.filter(wishlist=wishlist)
    
    
    print(wishlist_items)  
    
    
    
    context   = {'wishlist_items':wishlist_items,'wishlist':wishlist}
    return render(request,'wishlist.html',context)


@login_required
def toggle_wishlist(request):
    if request.method == 'POST':
    
        product_id = request.POST.get('product_id')
        print(product_id)
        wishlist = Wishlist.objects.get(user_id=request.user.id)
        product = get_object_or_404(Products, id=product_id)
        print(product)
        print(wishlist)
        
        if WishlistItems.objects.filter(wishlist=wishlist,product=product).exists():
            wishlist_item = WishlistItems.objects.get(wishlist=wishlist, product=product)
            wishlist_item.delete()
            status = 'removed'
        else:
            wishlist_item = WishlistItems.objects.create(wishlist=wishlist, product=product)
            wishlist_item.save()
            status = 'added'
        return JsonResponse({'status': status})
    else:
        return JsonResponse({'status': 'error'})


def delete_wishlist_item(request,id):
    
    item = WishlistItems.objects.get(id=id)
    item.delete()
    return redirect('wishlist')


def view_product(request,name): 
    
    
    details = Products.objects.get(product_name=name)
    sports = Sport.objects.all()
    brands = Brand.objects.all()
    
    if 'user' in request.session:
        cart      = Cart.objects.get(customer = request.user)
        cartitems = CartItem.objects.filter(cart= cart)
        total     = cartitems.count
        
    variants  = Variants.objects.filter(variant_product=details.id).order_by('-variant_size')
   

    return render(request,'product_details.html',locals()) 


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
     
    if request.method == 'POST':
        email = request.user
        data           = request.POST
        grand_total          = 0
     
        coupon_code    = data.get('code')
        sub_total      = data.get('sub_total')
        print(coupon_code)
        print(sub_total)
        try:
            coupon = Coupons.objects.get(coupon_code=coupon_code)
            request.session['coupon_code'] = coupon_code
            discount  = coupon.discount_price
            print(discount)
            
            grand_total = float(sub_total) - discount
            print(grand_total)
            return JsonResponse({
                'success': True,
                'grand_total': grand_total,
                'discount': discount,
                })
        
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
    
    
def searchProducts(request):
    if request.method=='POST':
        data           = request.POST
        searchterm     = data.get('search_term')
        print(searchterm)
        category_id    = request.GET.get('category_id')
        gender         = request.GET.get('gender')
        print(category_id)
        print(gender)
        products=Products.objects.filter(product_name__icontains = searchterm)
        if products:
            if gender:
                products = products.filter(product_gender=gender)   
            # if category_id:
            #     products = products.filter(product_category=category_id)
        else:
            products = Products.objects.filter(product_type__icontains = searchterm)   
            
        if 'store' in request.META.get('HTTP_REFERER'):
            # Render products in #product-list if search is being done from the store page
            return render(request,'product_list.html',{'products':products,'searchterm':searchterm,})
        else:
            # Render products on store.html page if search is being done from the home or index page
            return HttpResponseRedirect(reverse('shop') + '?search_term={}&gender={}&category_id={}'.format(searchterm, gender, category_id))   
        
    
def colorFilter(request):
    name     = request.GET.get('color')
    print(name)
    gender        = request.GET.get('gender')
    sport_id      = request.GET.get('sport_id')
    brand_id      = request.GET.get('brand_id')
    category_id   = request.GET.get('category_id')
    searchterm    = request.GET.get('searchterm')
    print(searchterm)
    product_names = request.GET.get('product_names', '').split(', ')
    
    print(gender)
    products = Products.objects.filter(product_color__icontains=name)
    if gender:
        products = products.filter(product_gender=gender)
    if sport_id:
        products = products.filter(product_sport=sport_id)
    if brand_id:
        products = products.filter(product_brand=brand_id)
    if category_id:
        products = products.filter(product_category=category_id)
    if searchterm:
        products = products.filter(product_name__icontains = searchterm )
    
    context = {'products': products}
    return render(request, 'product_list.html', context)



def sort_products(request):
    # Get the sorting criteria from the AJAX request
    sort_criteria = request.GET.get('sort_criteria')
    
    name     = request.GET.get('color')
    gender        = request.GET.get('gender')
    sport_id      = request.GET.get('sport_id')
    brand_id      = request.GET.get('brand_id')
    category_id   = request.GET.get('category_id')
    searchterm    = request.GET.get('searchterm')
    print(searchterm)
    product_names = request.GET.get('product_names', '').split(', ')
    
    print(gender)
    products = Products.objects.all()
    if name:
        products = products.filter(product_color__icontains=name)
    if gender:
        products = products.filter(product_gender=gender)
    if sport_id:
        products = products.filter(product_sport=sport_id)
    if brand_id:
        products = products.filter(product_brand=brand_id)
    if category_id:
        products = products.filter(product_category=category_id)
    if searchterm:
        products = products.filter(product_name__icontains = searchterm )

    # Query the database to get a list of products sorted by the specified criteria
    if sort_criteria == 'price_asc':
        products = products.order_by('product_price')
    elif sort_criteria == 'price_desc':
        products = products.order_by('-product_price')
    else:
        # Default to sorting by name if no criteria is specified
        products = products.order_by('product_name')

    # Serialize the list of products as JSON and return it as an AJAX response
    # data = {'products': list(products.values())}
    # return JsonResponse(data)

    context = {'products': products}
    return render(request, 'product_list.html', context)

def filter_products_by_price(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    name     = request.GET.get('color')
    gender        = request.GET.get('gender')
    print(gender)
    sport_id      = request.GET.get('sport_id')
    brand_id      = request.GET.get('brand_id')
    category_id   = request.GET.get('category_id')
    searchterm    = request.GET.get('searchterm')
    
    products = Products.objects.filter(product_price__gte=min_price, product_price__lte=max_price)
    print(products)
    if name:
        products = products.filter(product_color__icontains=name)
    if gender:
        products = products.filter(product_gender=gender)
    if sport_id:
        products = products.filter(product_sport=sport_id)
    if brand_id:
        products = products.filter(product_brand=brand_id)
    if category_id:
        products = products.filter(product_category=category_id)
    if searchterm:
        products = products.filter(product_name__icontains = searchterm )
    
    # products = products.filter(product_price__gte=min_price, product_price__lte=max_price)
    print("==========")
    print(products)
    # context = {'products': products}
    # return render(request, 'product_list.html', context)
    
    product_html = render(request, 'product_list.html', {'products': products}).content
    return JsonResponse({'html': product_html})