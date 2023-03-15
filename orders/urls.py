from django.urls import path
from . import views

urlpatterns = [
    path('review_order',views.review_order,name="review_order"),
    path('payment',views.payment,name="payment"),
    path('place_cod_order',views.place_cod_order,name="place_cod_order"),
    path('order_success_page',views.order_success_page,name="order_success_page"),
    path('order_details/<int:id>',views.order_details,name='order_details'),
    path('cancel_order/<int:id>',views.cancel_order,name='cancel_order'),
    path("payment_verification",views.payment_verification,name="payment_verification"),
    path('payment_success',views.payment_success,name='payment_success'),
]