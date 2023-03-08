from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_login,name='admin_login'),
    path('admin_dash',views.admin_dash,name='admin_dash'),
    path('admin-logout',views.admin_logout,name='admin_logout'),
    
    #====================User management=====================#
    path('user_list',views.user_list,name='user_list'),
    path('block_user/<int:id>',views.block_user,name='block_user'),
    path('unblock_user/<int:id>',views.unblock_user,name='unblock_user'),
    
    #====================Product management=====================#
    path('product_list',views.product_list,name='product_list'),
    path('add_product',views.add_product,name='add_product'),
    path('search_product',views.search_product,name='search_product'),
    path('edit-product/<int:id>',views.edit_product,name='edit_product'),
    path('delete_product/<int:id>',views.delete_product,name='delete_product'),
    
    #====================Variants management=====================#
    path('variant_list',views.variant_list,name='variant_list'),
    path('add_variant',views.add_variant,name='add_variant'),
    path('search_variant',views.search_variant,name='search_variant'),
    path('edit-variant/<int:id>',views.edit_variant,name='edit_variant'),
    path('delete_variant/<int:id>',views.delete_variant,name='delete_variant'),
   
    
    #====================Category management=====================#
    path('category_list',views.category_list,name='category_list'),
    path('add_category',views.add_category,name='add_category'),  
    path('delete_category/<int:id>',views.delete_category,name='delete_category'),
   
    #====================Brand management=====================# 
    path('brand_list',views.brand_list,name='brand_list'),
    path('add_brand',views.add_brand,name='add_brand'),  
    path('delete_brand/<int:id>',views.delete_brand,name='delete_brand'), 
   
    #====================Sport management=====================# 
    path('sport_list',views.sport_list,name='sport_list'),
    path('add_sport',views.add_sport,name='add_sport'),  
    path('delete_sport/<int:id>',views.delete_sport,name='delete_sport'), 
    
    #====================Banner management=====================# 
    path('orders',views.orders,name='orders'),
    
    #====================Banner management=====================# 
    path('banners',views.banners,name='banners'),
    path('add_banners',views.add_banners,name='add_banners'),
]
