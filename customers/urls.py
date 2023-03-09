from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register',views.register_view,name='register'),
    path('verify_signup',views.verify_signup,name='verify_signup'),
    path('user_login',views.user_login,name='user_login'),
    path('logout',views.logout,name='logout'),
    path('home',views.home,name='home'),
    path('profile',views.profile,name='profile'),
    path('upload_profile_img',views.upload_profile_img,name='upload_profile_img'),
    path('update_username',views.update_username,name='update_username'),
    path('update_password',views.update_password,name='update_password'),
    path('address',views.address,name='address'),
    path('my_orders',views.my_orders,name='my_orders'),
    path('add_address',views.add_address,name='add_address'),
    path('delete_address/<int:id>',views.delete_address,name='delete_address'),
]
