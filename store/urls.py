from django.urls import path
from . import views

urlpatterns = [
     path('cart',views.cart,name='cart'),
     
     path('mens',views.mens_store,name='men'),
     path('mens_sport/<id>',views.mensSport,name='mens_sport'),
     path('mens_brands/<id>',views.mensBrands,name='mens_brands'),
     
     path('women',views.womens_store,name='women'),
     path('womens_sport/<id>',views.womensSport,name='womens_sport'),
     path('womens_brands/<id>',views.womensBrands,name='womens_brands'),
    
     
   
     path('product_details/<int:id>',views.product_details,name="product_details"),
     path('search_products',views.search_products,name="search_products"),


     path('add_to_cart',views.add_to_cart,name='add_to_cart'),
     path('update_cart_quantity',views.update_cart_quantity,name="update_cart_quantity"),
     path('delete_cartitem/<int:id>',views.delete_cartitem,name="delete_cartitem"),
     
     path('checkout',views.checkout,name="checkout"),
     path('add_checkout_address',views.add_checkout_address,name="add_checkout_address"),
     path('delete_address2/<int:id>',views.delete_address2,name='delete_address2'),
     path('redeem_coupon',views.redeem_coupon,name='redeem_coupon'),
]
