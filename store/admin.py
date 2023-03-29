from django.contrib import admin
from .models import Products,Cart,Category,Brand,Sport,Variants,Banners,CartItem,Size,Image,Coupons
# Register your models here.

admin.site.register(Products)
admin.site.register(Variants)
admin.site.register(Cart)
admin.site.register(Size)
admin.site.register(Banners)
admin.site.register(CartItem)
admin.site.register(Image)
admin.site.register(Coupons)
admin.site.register(Category)
admin.site.register(Brand)
