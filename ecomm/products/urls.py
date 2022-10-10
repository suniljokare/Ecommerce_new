from django.urls import path,include
from django.conf import settings
from .views import *

product_details
urlpatterns = [
    # path('',add_to_wishlist, name = 'add_to_wishlist'),
    path('product_details/<int:id>/',product_details, name = 'product_details'),
    path('add_to_cart/<int:id>/',add_to_cart,name='add_to_cart'),
    path('cart/',cart,name='cart'),
    path('remove_cart_item/<id>/',remove_cart_item,name='remove_cart_item'),
    path('place_order/<total>/',place_order,name='place_order'),
    path('order_summary/',order_summary,name='order_summary'),
    path('order_history/',order_history,name='order_history'),
    path('success/',success,name='success'),


]

