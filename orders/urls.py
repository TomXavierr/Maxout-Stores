from django.urls import path
from . import views

urlpatterns = [
    path('place_order',views.place_order,name="place_order"),
    path('order_success_page',views.order_success_page,name="order_success_page"),
    path('order_details/<int:id>',views.order_details,name='order_details'),
    path('cancel_order/<int:id>',views.cancel_order,name='cancel_order'),
]