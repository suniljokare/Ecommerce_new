from django import template
from products.models import *
from django.contrib import messages
from datetime import datetime, timedelta


register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product  , cart):
    keys = cart.keys()

    for id in keys:
        if int(id) == product.id:
            return True
    return False


@register.filter(name='cart_quantity')
def cart_quantity():
    cart =Cart.objects.all().count()
    
    return cart if cart >0 else 0


@register.filter(name='price_total')
def price_total(cart):
    return cart.product.price * cart.quantity


@register.filter(name='delivery_date')
def delivery_date(date):
    delivery_date = str(date) + str(timedelta(days=4))
    return delivery_date


@register.filter(name='total_cart_price')
def total_cart_price(carts, coupon=None):
    sum = 0 
    
    for cart in carts:
        sum += price_total(cart)
    
    if coupon is not None:
        if coupon.minimum_amount < sum:
            return sum - coupon.discount_price  

    return sum


            