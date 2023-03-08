from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from customers.models import Account
from store.models import Products,Brand,Sport,Category,Variants,Banners,Size,Image
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from orders.models import Orders

# Create your views here.
@cache_control(no_cache = True,must_revalidate = False,no_store=True) 
@login_required(login_url='admin_login')
def admin_dash(request):
    if request.user.is_superuser:
        return render(request,'admin_dashboard.html')
    else:
        return redirect('home')
  
    

def admin_login(request):

    if request.method== 'POST':
        email = request.POST['email']
        password = request.POST['password']
       
        if email and password:
            admin=authenticate(email=email,password=password)
            if admin and admin.is_superuser:
                # request.session['admin'] = password
                auth.login(request,admin)
                return redirect('admin_dash')
            else:
                messages.info(request,'Invalid email or password')
                return redirect('admin_login')
        else:
            messages.info(request,'Enter your email and password')
            return redirect('admin_login')
    elif not request.user.is_authenticated:
        return render(request,'admin_login.html')
    else:
        return redirect('admin_dash')
def admin_logout(request):
    auth.logout(request)
    # del request.session['admin']
    return redirect('admin_login')



    
def user_list(request):
    if request.user.is_superuser: 
        users   =  Account.objects.all().order_by('id')
        context = {'users': users}
        return render(request,'users_list.html',context)
    else:
        return redirect('home')

def block_user(request,id):
    user=Account.objects.get(id=id)
    user.is_blocked = True
    user.save()
    return redirect('user_list')

def unblock_user(request,id):
    user=Account.objects.get(id=id)
    user.is_blocked = False
    user.save()
    return redirect('user_list')


#=====================================Functions for products============================================

def product_list(request):
    if request.user.is_superuser: 
        products   =  Products.objects.all().order_by('id')
        
    
        # items_per_page = 4
        # paginator = Paginator(products, items_per_page)
        # page_number = request.GET.get('page')

        return render(request,'products_list.html',{'products':products})
    
    else:
        return redirect('home')
    
def add_product(request):
    
    if request.method == 'POST':
        product_name          = request.POST['product_name']
        product_description   = request.POST['description']
        product_brand         = request.POST['brand']
        category              = request.POST['category']
        product_image         = request.FILES.get('image')
        gender                = request.POST['gender']
        color                 = request.POST['color']
        product_type          = request.POST['product_type']
        price                 = request.POST['price']
        sport                 = request.POST['sport']
        images                = request.FILES.getlist('images')
         
        if product_name and product_description and product_brand and product_image and product_type and color and price :
            product = Products.objects.create(
                product_name          = product_name,
                product_description   = product_description,
                product_brand         = Brand.objects.get(brand_name=product_brand),
                product_category      = Category.objects.get(category_name=category),
                product_sport         = Sport.objects.get(sport_name=sport),
                product_gender        = gender,
                product_color         = color,
                product_type          = product_type,
                product_price         = price,
                product_image         = product_image,

                )
            product.save();
            for i in reversed(images):
                    image = Image.objects.create(
                        product = Products.objects.get(product_name=product_name ),
                        # variant = Variants.objects.get(id = variant.pk),
                        image = i,
                    )
                    
            
            return redirect('product_list')
        else:
            messages.info(request,'Input all fields')
            return redirect('add_product')
            
    # categories = Category.objects.all()
    brands      = Brand.objects.all()
    categories  = Category.objects.all()
    sports      = Sport.objects.all()
   
    
    context  = {'sports':sports,
        'brands':brands,
        'categories':categories,
        'Products':Products, 
       }
    return render(request,'add_product.html',context)
    
def search_product(request):
    if request.method=='GET':
        searchterm =request.GET.get('searchterm')
        print(searchterm)
        products=Products.objects.filter(product_name__icontains = searchterm)
        return render(request,'products_list.html',{'products':products})
    else:
        print('Nothing similar')
        return redirect('product_list')

@login_required(login_url='admin_login')
def edit_product(request,id):
    product    = Products.objects.get(id=id)
    brands     = Brand.objects.all()
    categories = Category.objects.all()
    sports     = Sport.objects.all()
   
    
    if request.method == 'POST':
        # Update the product with the data from the form
        product_name          = request.POST['product_name']
        product_description   = request.POST['description']
        product_brand         = request.POST['brand']
        product_sport         = request.POST['sport']
        product_category      = request.POST['category']
        product_image         = request.FILES.get('image')
        product_gender        = request.POST['gender']
        product_type          = request.POST['product_type']
        price                 = request.POST['price']
        color                 = request.POST['color']
        images                = request.FILES.getlist('images')
        
        
        product.product_name        = product_name
        product.product_description = product_description
        product.product_brand       = Brand.objects.get(brand_name=product_brand)
        product.product_image       = product_image
        product.product_sport       = Sport.objects.get(sport_name=product_sport)
        product.product_category    = Category.objects.get(category_name = product_category)
        product.product_gender      = product_gender
        product.product_type        = product_type
        product.product_price       = price
        product.product_color       = color
    
    
        product.save()
        image   = Image.objects.filter(product = product.id)   
        image_ids = [i.pk for i in image]
            
        for image, id in zip(reversed(images), image_ids):
            
            img = Image(
                id = Image.objects.get(id = id).pk,
                image = image,
                product = Products.objects.get(product_name=product_name ),
            )
            img.save()
        
        return redirect('product_list')
    
    
    else:
        # Render the product edit form
        brands     = Brand.objects.all()
        context = {'product': product ,'brands':brands ,'categories':categories ,'sports':sports , 'Products':Products}
        return render(request, 'edit_product.html', context)

@login_required(login_url='admin_login')
def delete_product(request,id):
    product=Products.objects.get(id=id)
    product.delete()
    return redirect('product_list')

#================================Functions for categories=======================================

def variant_list(request):
    if request.user.is_superuser: 
        variants   =  Variants.objects.all().order_by('id')
        
        
        items_per_page = 10
        paginator = Paginator(variants, items_per_page)
        page_number = request.GET.get('page')
        page_variants = paginator.get_page(page_number)
        
        return render(request,'variants.html',{'variants':page_variants})
    else:
        return redirect('home')

def add_variant(request):
    products   = Products.objects.all()
    sizes      = Size.objects.all()
     
    context = {
        'sizes':sizes,
        'products':products, 
    }
    
    if request.method == 'POST':
        product               = request.POST['product']
        stock                 = request.POST['stock']
        size                  = request.POST['size']
        
        
        if  product and size and  stock :
            if Variants.objects.filter(variant_product=Products.objects.get(product_name=product),variant_size=Size.objects.get(size=size)).exists():
                messages.info(request,'Variant already exists')
                return redirect('add_variant')
            
            
            else:
                variant = Variants.objects.create(
                    variant_product       = Products.objects.get(product_name=product),
                    variant_stock         = stock,
                    variant_size          = Size.objects.get(size=size),
                    )
                variant.save();
                return redirect('variant_list')
            
            
        else:
            messages.info(request,'Input all fields')
            return redirect('add_variant')
            
    
    return render(request,'add_variant.html',context)



@login_required(login_url='admin_login')
def edit_variant(request,id):
    variant      = Variants.objects.get(id=id)
    product      = variant.variant_product
    print(product)
    if request.method == 'POST':
        # Update the product with the data from the form
        

        size                  = request.POST['size']
        stock                 = request.POST['stock']
   
        if  product and size and stock :
            # if Variants.objects.filter(variant_product=Products.objects.get(product_name=product),variant_color=color,variant_size=Size.objects.get(size=size)).exists():
            #     messages.info(request,'Variant already exists')
            #     return redirect('add_variant')
            # else:
       
                variant.variant_product     = Products.objects.get(id = variant.variant_product.id)
                variant.variant_size        = Size.objects.get(size=size)
                variant.variant_stock       = stock
                variant.save()
        return redirect('variant_list')
    
    else:
        # Render the product edit form
        sizes      = Size.objects.all()
        
        context = {
            'variant':variant,
            'variants':Variants,
            'sizes':sizes,
            }
        return render(request, 'edit_variants.html', context)

@login_required(login_url='admin_login')
def delete_variant(request,id):
    variant=Variants.objects.get(id=id)
    variant.delete()
    return redirect('variant_list')

def search_variant(request):
    if request.method=='GET':
        searchterm =request.GET.get('searchterm')
        print(searchterm)
        variants=Variants.objects.filter(variant_name__icontains = searchterm)
        return render(request,'variants.html',{'variants':variants})
    else:
        print('Nothing similar')
        return redirect('variant_list')

#================================Functions for Banners=======================================

def banners(request):
    if request.user.is_superuser: 
        banners   =  Banners.objects.all().order_by('id')
        return render(request,'banners.html',{'banners':banners})
    else:
        return redirect('home')
    
def add_banners(request):
    if request.method == 'POST':
        name                   = request.POST['name']
        banner                = request.FILES.get('banner')

        if banner and name:
            banner = Banners.objects.create(
                name      = name,
                banners   = banner    
                )
        return redirect('banners')
   
    return render(request,'add_banners.html')

#================================Functions for categories=======================================

def category_list(request):
    if request.user.is_superuser:
        categories   =  Category.objects.all
        return render(request,'categories_list.html',{'categories':categories})
    else:
        return redirect('home')

def add_category(request):
    if request.method == 'POST':
        category_name        = request.POST['category_name']
    
        
        if category_name :
            if Category.objects.filter(category_name=category_name).exists():
                messages.info(request,'Category already exists')
                return redirect('add_category')
            else:
                category = Category.objects.create(category_name=category_name)
                category.save();
                return redirect('category_list')
        else:
            messages.info(request,'Input all fields')
            return redirect('add_category')
    return render(request,'add_categories.html')

@login_required(login_url='admin_login')
def delete_category(request,id):
    category=Category.objects.get(id=id)
    category.delete()
    return redirect('category_list')


#=====================================Functions for brands============================================

def brand_list(request):
    if request.user.is_superuser:
        brands   =  Brand.objects.all
        return render(request,'brand_list.html',{'brands':brands})
    else:
        return redirect('home')

@login_required(login_url='admin_login')
def add_brand(request):
    if request.method == 'POST':
        brand_name        = request.POST['brand_name']
        
        if brand_name :
            if Brand.objects.filter(brand_name=brand_name).exists():
                messages.info(request,'Brand name already exists')
                return redirect('add_brand')
            else:
                brand = Brand.objects.create(brand_name=brand_name)
                # brand.save();
                return redirect('brand_list')
        else:
            messages.info(request,'Input all fields')
            return redirect('add_brand')
    return render(request,'add_brand.html')

@login_required(login_url='admin_login')
def delete_brand(request,id):
    brand=Brand.bjects.get(id=id)
    brand.delete()
    return redirect('brand_list')



#=====================================Functions for Sports============================================

def sport_list(request):
    sports   =  Sport.objects.all
    return render(request,'sport_list.html',{'sports':sports})

@login_required(login_url='admin_login')
def add_sport(request):
    if request.method == 'POST':
        sport_name        = request.POST['sport_name']
        
        if sport_name:
            if Sport.objects.filter(sport_name=sport_name).exists():
                messages.info(request,'sport name already exists')
                return redirect('add_sport')
            else:
                sport = Sport.objects.create(sport_name=sport_name)
                # sport.save();
                return redirect('sport_list')
        else:
            messages.info(request,'Input all feilds')
            return redirect('add_sport')
    return render(request,'add_sport.html')

@login_required(login_url='admin_login')
def delete_sport(request,id):
    sport=Sport.objects.get(id=id)
    sport.delete()
    return redirect('sport_list')

@login_required(login_url='admin_login')
def orders(request):
    orders    = Orders.objects.all
    return render(request,'orders_list.html',{'orders':orders})
