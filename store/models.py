from django.db import models
from customers.models  import Account

# Create your models here.

class Products(models.Model):
    GENDER_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
    ]
    product_name              = models.CharField(max_length=100)
    product_description       = models.TextField(max_length=200)
    product_brand             = models.ForeignKey("Brand", on_delete=models.CASCADE, default=False , null=False)
    product_category          = models.ForeignKey("Category", on_delete=models.CASCADE, default=False , null=False)
    product_gender            = models.CharField(max_length=10,choices=GENDER_CHOICES,default='Men')
    product_image             = models.ImageField(upload_to='photos/',null=False,blank=False)
    product_sport             = models.ForeignKey("Sport", on_delete=models.CASCADE, default=False , null=False)
    product_color             = models.CharField(max_length=30, null=False)
    product_type              = models.CharField(max_length=30, null=False)
    product_price             = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    
    def __str__(self):
        return str(self.pk)
    
class Variants(models.Model):
    variant_product           = models.ForeignKey(Products,related_name='variants', on_delete=models.CASCADE)
    variant_size              = models.ForeignKey("Size", on_delete=models.CASCADE, default=False , null=False)
    variant_stock             = models.IntegerField()
    created_on                = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    
    def __str__(self):
        return str(self.pk)
    
    
    
class Image(models.Model):
    id = models.BigAutoField(primary_key=True,blank=True)
    product = models.ForeignKey(Products,related_name='images',on_delete=models.CASCADE,null=True,blank=True)
  
    image = models.ImageField(upload_to='productphotos/',blank=True,null=True)


    def __str__(self):
        return str(self.pk)   



class Size(models.Model):
    size                       = models.CharField(max_length=20)
         

class Cart(models.Model):
    customer                   = models.ForeignKey(Account,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    @property
    def cart_total(self):
        cartitems = self.cartitem_set.all()
        total     = sum([item.get_total for item in cartitems])
        return total
    
    @property
    def get_cart_items(self):
        cartitems = self.cartitem_set.all()
        total     = sum([item.product_qty for item in cartitems])
        return total

    
class CartItem(models.Model):
    product                    = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart                       = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_qty                = models.IntegerField(default=1)
    size                       = models.CharField(max_length=10)
    
    @property
    def get_total(self):
        return self.product.product_price * self.product_qty
   

class Coupons(models.Model):
    coupon_code = models.CharField(max_length=10)
    expired = models.BooleanField(default=False)
    discount_price = models.FloatField(default=100)
    minimum_amount = models.FloatField(default=500)
    expiry_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.coupon_code

class Wishlist(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    
class WishlistItems(models.Model):
    product                    = models.ForeignKey(Products, on_delete=models.CASCADE)
    wishlist                   = models.ForeignKey(Wishlist, on_delete=models.CASCADE)

class Banners(models.Model):
    name                     = models.CharField(max_length=30,null=False)
    banners                  = models.ImageField(upload_to='photos/',null=False,blank=False)
    
    
class Category(models.Model):
    category_name              = models.CharField(max_length=100)
  
  
  
class Brand(models.Model):
    brand_name                 = models.CharField(max_length=100)
  
  
class Sport(models.Model):
    sport_name                 = models.CharField(max_length=100)

class Wallet(models.Model):
    user                = models.ForeignKey(Account,on_delete=models.CASCADE)
    balance             = models.DecimalField(max_digits=8, decimal_places=2, default=0)