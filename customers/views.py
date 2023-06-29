from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login, authenticate,logout,update_session_auth_hash
from .models import Account,Addresses
from store.models import *
from orders.models import *

from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control,never_cache
from django.utils.decorators import method_decorator
from django.db.models import Sum
from functools import wraps

import smtplib 
import secrets
import re

# Create your views here.


def check_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff == False and request.user.is_superuser == False and request.user.is_active == True and request.user.is_blocked == False:
            return view_func(request, *args, **kwargs)
        else:
            messages.info(request,'Your account an admin')
            return redirect('user_login')
    return wrapper_func


def handle_cart(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(customer=request.user)
            except Cart.DoesNotExist:
                cart = None
        else:
            cart = None

        response = view_func(request, cart=cart, *args, **kwargs)
        return response

    return wrapper


@cache_control(no_cache = True,must_revalidate = False,no_store=True)
def index(request):
    if request.user.is_authenticated and not request.user.is_superuser:
       return redirect('home')
    top_products = OrderItem.objects.values('product__product_name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    top_product_names = [item['product__product_name'] for item in top_products]
    top_products_obj = Products.objects.filter(product_name__in=top_product_names)
    print(top_products)
    print(top_product_names)
    
    print(top_products_obj)
    
    context = {
        'top_products': top_products_obj,
        'main_banner':  Banners.objects.get(id=1).banners,
        'sports':       Sport.objects.all(),
        'categories':   Category.objects.all(),
        'brands':       Brand.objects.all() ,
        'Products':     Products}
    return render(request,'index.html',context)


@cache_control(no_cache = True,must_revalidate = False,no_store=True)
def register_view(request):
    if 'user' in request.session :
        return redirect('home')
    
    if request.method =='POST':
        email =request.POST['email']
        username =request.POST['username']
        passwrod1 =request.POST['password1']
        password2 =request.POST['password2']
        
        if email and username and passwrod1 and password2:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                # email is invalid
                error_message = "Please enter a valid email address."
                return render(request, 'signup.html', {'error_message': error_message})
            
            elif passwrod1 == password2:
                if Account.objects.filter(username=username).exists():
                    messages.info(request,'Username Taken')
                    return redirect('register')
                elif Account.objects.filter(email=email).exists():
                    messages.info(request,'Email Taken')
                    return redirect('register')
                else:
                    message = generate_otp()
                    sender_email  = "maxoutstores1@gmail.com"
                    receiver_mail = email
                    password      = "urxtynwjuveqitvf"
                   
                    server        = smtplib.SMTP("smtp.gmail.com",587)
                    server.ehlo()
                    server.starttls()
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_mail, message)
                    server.quit
                    
                    user = Account.objects.create_user(username=username,password=passwrod1,email=email)
                    
                    user.save()
                    request.session['email'] = email
                    request.session['otp'] = message
                    hello = request.session['email']
                    print(hello)
                   
                    return redirect('verify_signup',)
            else:
                messages.info(request,'Password not matching')
                return redirect('register')
        else:
            messages.info(request,'Input every details')
            return redirect('register')
    else:
        return render(request,'signup.html') 
    
    
def generate_otp(length=6):
    #generate OTP with specific length
    return ''.join(secrets.choice("0123456789") for i in range(length))     
   

@cache_control(no_cache = True,must_revalidate = False,no_store=True)  
def verify_signup(request):
    
    if request.method == "POST":
     
        user = Account.objects.get(email=request.session['email'])
        x  = request.session.get('otp')
        print(user)
        OTP = request.POST['otp']
        
        if OTP == x:
            user.is_verified = True
            user.save()
            cart = Cart.objects.create(customer=user)
            wishlist  = Wishlist.objects.create(user=user)
            del request.session['email'] 
            del request.session['otp']
            
            auth.login(request,user)
            return redirect('home')
        else:
            user.delete()
            messages.info(request,"invalid otp")
            return redirect('register')
    return render(request,'signup_verify.html') 
    
    
@never_cache
def user_login(request):
    if 'user' in request.session :
        return redirect('home')
    
    if request.method== 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
       
        if email and password:
            user=authenticate(email=email,password=password)
            if user is not None and not user.is_blocked :
                if  user.is_verified:
                    print(user)
                    request.session['user_type'] = 'user'
                    login(request,user)
                    return redirect('home')
                else:
                    messages.info(request,'Your account is not verified')
                return redirect('user_login')
            else:
                messages.info(request,'Your account has been blocked')
                return redirect('user_login')
        else:
            messages.info(request,'Enter every details')
            return redirect('user_login')
    else:
         return render(request,'signin.html')
    
    
def logout(request):
    auth.logout(request)
    return redirect(index)

   
@login_required(login_url='user_login') 
@check_user
@handle_cart
def home(request,cart =None):
    top_products = OrderItem.objects.values('product__product_name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    top_product_names = [item['product__product_name'] for item in top_products]
    top_products_obj = Products.objects.filter(product_name__in=top_product_names)
   
    
    context = {
        'top_products': top_products_obj,
        'main_banner':  Banners.objects.get(id=1).banners,
        'cart':         cart,
        'sports':       Sport.objects.all(),
        'categories':   Category.objects.all(),
        'brands':       Brand.objects.all() ,
    }
    return render(request,'home.html',context)
  
@handle_cart
@login_required(login_url='user_login') 
@check_user
def profile(request, cart = None):
    context = {
        'main_banner':  Banners.objects.get(id=1).banners,
        'cart':         cart,
        'sports':       Sport.objects.all(),
        'brands':       Brand.objects.all() ,
        'user':         request.user,
        'Products':     Products,
        }
   
    return render(request,'user_profile.html',context)
@handle_cart
@login_required(login_url='user_login') 
def update_username(request,cart = None):
    context = {
    'main_banner':  Banners.objects.get(id=1).banners,
    'cart':         cart,
    'sports':       Sport.objects.all(),
    'brands':       Brand.objects.all() ,
    'user':         request.user,
    'Products':     Products,
    }
   
    if request.method == 'POST':
        # Get the new username from the form data
        current_username = request.user.username
        new_username     = request.POST.get('new_username')
    
        # Update the user's username 
        if new_username and current_username: 
            user = request.user
            if Account.objects.filter(username=new_username).exists():
                messages.info(request,'Username already exists')
                return redirect('update_username') 
            else:
                user.username = new_username
                user.save()
                update_session_auth_hash(request, user)
        return redirect('profile')
    
    return render(request, 'update_user.html',context)

@handle_cart
def upload_profile_img(request, cart = None):
    context = {
    'main_banner':  Banners.objects.get(id=1).banners,
    'cart':         cart,
    'sports':       Sport.objects.all(),
    'brands':       Brand.objects.all() ,
    'user':         request.user,
    }
   
    user           = request.user
    if  request.method == 'POST':
        profile_image         = request.FILES.get('image')
        user.profile_image = profile_image
        user.save()
        return redirect('profile')
    return render(request, 'upload_profile.html',context)
    
@handle_cart
@login_required(login_url='user_login') 
def update_password(request,cart=None):
    context = {
        'main_banner':  Banners.objects.get(id=1).banners,
        'cart':         cart,
        'sports':       Sport.objects.all(),
        'brands':       Brand.objects.all() ,
        'user':         request.user,
        'Products':     Products,
        }
   
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password1    = request.POST.get('new_password1')
        new_password2    = request.POST.get('new_password2')
        user=request.user
         
        if new_password2 == new_password1:
            if current_password == new_password1: 
                messages.info(request,'This is your previous password. Enter a new one.')
                return redirect('update_password')
            else:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)
                return redirect('profile')
        else:
            messages.info(request,'Enter the new password correctly in both columns')
            return redirect('update_password')
    return render(request, 'update_password.html',context)

@handle_cart
@login_required(login_url='user_login') 
def address(request, cart= None):
    context = {
        'main_banner':  Banners.objects.get(id=1).banners,
        'cart':         cart,
        'sports':       Sport.objects.all(),
        'brands':       Brand.objects.all() ,
        'user':         request.user,
        'addresses':    Addresses.objects.filter(user_id=request.user),
        }

    return render(request, 'user_address.html', context)

@handle_cart
@cache_control(no_cache = True,must_revalidate = False,no_store=True)
def add_address(request, cart= None):
    context = {
    'main_banner':  Banners.objects.get(id=1).banners,
    'cart':         cart,
    'sports':       Sport.objects.all(),
    'brands':       Brand.objects.all() ,
    'user':         request.user,
    'Products':     Products,
    }

    user = request.user
    user_id = user.id
    
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
                return render(request, 'add_address.html', {'error_message': error_message})
            
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
            return redirect('address')
        else:
            messages.info(request,'Input all fields')
            return redirect('add_address')
    else:
        return render(request, 'add_address.html',context)
  
@handle_cart
@cache_control(no_cache = True,must_revalidate = False,no_store=True)
def edit_address(request,id , cart = None):
    user     = request.user
    user_id  = user.id
    address  =    Addresses.objects.get(user_id=user_id)
    
    context = {
    'main_banner':  Banners.objects.get(id=1).banners,
    'cart':         cart,
    'sports':       Sport.objects.all(),
    'brands':       Brand.objects.all() ,
    'user':         request.user,
    'Products':     Products,
    'address':      address,
    }
        
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
                # mobile is invalid
                error_message = "Please enter a valid Mobile number."
                return render(request, 'edit_address.html', {'error_message': error_message})
            
            else:
               
                address.first_name   = first_name
                address.last_name    = last_name
                address. house_name   = house_name
                address.street_name  = street_name
                address.city         = city
                address.district     = district
                address.state        = state
                address.pincode      = pincode
                address.mobile       = mobile
                address.user_id      = Account.objects.get(id=user_id)
                address.save()
                return redirect('address')
        else:
            messages.info(request,'Input all fields')
            return redirect('edit_address')
    else:
        return render(request, 'edit_address.html',context)
    
def delete_address(request,id):
    address = Addresses.objects.get(id=id)
    address.delete()
    return redirect('address')


@handle_cart
@login_required(login_url='user_login') 
def my_orders(request,cart = None):
    context = {
        'main_banner':  Banners.objects.get(id=1).banners,
        'cart':         cart,
        'sports':       Sport.objects.all(),
        'brands':       Brand.objects.all() ,
        'user':         request.user,
        'orders':      Orders.objects.filter(user = request.user).order_by('-id'),
        }
   
    return render(request,'my_orders.html',context)

@handle_cart
@login_required(login_url='user_login') 
def order_details(request,id,cart = None):
    
    order       = Orders.objects.get(id=id)
    order_items = order.orderitem_set.all()
    payment     = Payment.objects.get(order=order)
    context = {
    'main_banner':  Banners.objects.get(id=1).banners,
    'cart':         cart,
    'sports':       Sport.objects.all(),
    'brands':       Brand.objects.all() ,
    'user':         request.user,
    'order':        order ,
    'order_items':  order_items,
    'payment':      payment,
    }
    return render(request,'order_details.html',context)
