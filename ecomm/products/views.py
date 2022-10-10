from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import *
from django.views import View
from .templatetags.cart import *
from django.contrib import messages
from .forms import *

import razorpay

# from products.models WhisList



def product_details(request,id):
    product = Product.objects.get(id=id)
    return render(request, 'products/product_details.html', {'product':product})


def cart(request):
    
    ids = list(request.session.get('cart').keys())
    products = Product.objects.filter(id__in =ids)
    total = total_cart_price(products, request.session.get('cart'))

    if request.POST:
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
        

        if not coupon_obj.exists():
            messages.warning(request, 'Invalid Coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if total_cart_price(products, request.session.get('cart')) < coupon_obj[0].minimum_amount:
            messages.warning(request, f'amount should be greater than {coupon_obj[0].minimum_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj[0].is_expired:
            messages.warning(request, f'coupon expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        total = total_cart_price(products, request.session.get('cart'), coupon_obj[0])

        if 'total' not in request.session:
            request.session['total'] = total
    
        coupon_obj.update(is_expired = True)
        coupon_obj[0].save()
        messages.success(request, 'Coupon applied')
        return render(request, 'products/cart.html',{'products':products,'total':total})

        # Coupon.objects.get('')
        # cart_obj.coupon = coupon_obj[0]
        # cart_obj.save()
        # messages.success(request, 'Coupon applied')
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  

    if 'total' not in request.session:
            request.session['total'] = total

    return render(request, 'products/cart.html',{'products':products,'total':total})


# class add_to_cart(View):

#     def post(self , request):
#         product = request.POST.get('product')
#         remove = request.POST.get('remove')
#         cart = request.session.get('cart')
#         if cart:
#             quantity = cart.get(product)
#             if quantity:
#                 if remove:
#                     if quantity<=1:
#                         cart.pop(product)
#                     else:
#                         cart[product]  = quantity-1
#                 else:
#                     cart[product]  = quantity+1
#             else:
#                 cart[product] = 1
#         else:
#             cart = {}
#             cart[product] = 1

#         request.session['cart'] = cart
#         print('cart' , request.session['cart'])
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#     def get(self , request):
#         print(request,'***********')
#         product = Product.objects.get(id=id)
#         return render(request, 'products/product_details.html', {'product':product})


def add_to_cart(request,id):

    product = request.POST.get('product')
    remove = request.POST.get('remove')
    cart = request.session.get('cart')

    if cart:
        quantity = cart.get(product)
        if quantity:
            if remove:
                if quantity<=1:
                    cart.pop(product)
                else:
                    cart[product]  = quantity-1
            else:
                cart[product]  = quantity+1
        else:   
            cart[product] = 1
    else:
        cart = {}
        cart[product] = 1

    request.session['cart'] = cart
    print('cart' , request.session['cart'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart_item(request, id):
    cart = request.session.get('cart')
    if id in cart:
        del cart[id]  
        request.session["cart"] = cart
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
def place_order(request,total):

    ids = list(request.session.get('cart').keys())
    products = Product.objects.filter(id__in =ids)
    total = total_cart_price(products, request.session.get('cart'))
    orders = None

    fm = AddressForm()
    if request.method == 'POST':
        fm = AddressForm(request.POST)
        if fm.is_valid():
            name = fm.cleaned_data['name']
            mobile = fm.cleaned_data['mobile']
            pincode = fm.cleaned_data['pincode']
            locality = fm.cleaned_data['locality']
            address = fm.cleaned_data['address']
            city = fm.cleaned_data['city']
            state = fm.cleaned_data['state']
            landmark = fm.cleaned_data['landmark']
            alternate_mobile = fm.cleaned_data['alternate_mobile']
            # payment_method = fm.cleaned_data['payment']
            order = Order(user=request.user,  grand_total =request.session.get('total') ,name=name,mobile=mobile,pincode=pincode,locality=locality,address=address,city=city,state=state,landmark=landmark,alternate_mobile=alternate_mobile,shipping_charges ='100')
            order.save()
            
            orders = Order.objects.filter(user=request.user)
            return render(request, 'products/checkout2.html',{'form':fm, 'products':products, 'orders':orders,'total':total})
        fm = AddressForm()
        return render(request, 'products/checkout2.html',{'form':fm, 'products':products, 'orders':orders,'total':total})
    
    return render(request, 'products/checkout2.html',{'form':fm,'products':products, 'orders':orders, 'total':total})



def order_summary(request):
    order = Order.objects.get(user =request.user,status=False)
    ids = list(request.session.get('cart').keys())
    products = Product.objects.filter(id__in =ids)
    total = total_cart_price(products, request.session.get('cart'))

    for i, j in request.session.get('cart').items():
        order_details = OrderDetails ( order = order, product = Product.objects.get(id =i), 
                                quantity = j , 
                                amount= j*Product.objects.get(id =i).price )
        order_details.save()

    (request.session.get('cart')).clear()
    # (request.session.get('total')).clear()
     
    request.session.flush() 
    request.session.modified = True
    order.status = True
    order.save()
   
    orders = order.orderdetails.all()
    
    if request.POST.get('payment') == 'cod':
        messages.success(request, 'Order Placed')
        return render(request, 'products/order.html', {'orders':orders, 'total': order.grand_total})
    
    if request.POST.get('payment') == 'paypal':
        messages.success(request, 'Order Placed')
        return render(request, 'products/paypal.html', {'orders':orders, 'total': order.grand_total})
            
    if request.POST.get('payment') == 'razorpay':
        client = razorpay.Client(auth = ('rzp_live_TaVYIwbR7EH1kb', 'GrlyZZ55UACInguj0KUSOjnG'))
        payment = client.order.create({'amount': int(order.grand_total) *100, 'currency': 'INR', 'payment_capture':1})
        print(int(order.grand_total) *100,'***********************')
        messages.success(request, 'Order Placed')
        return render(request, 'products/razorpay.html', {'orders':orders, 'total': int(order.grand_total)*100, 'payment':payment})


def order_history(request):
    orders = Order.objects.filter(user =request.user, status = True)
    products = OrderDetails.objects.filter(order =orders[0])
    return render(request, 'products/order_history.html', {'orders':orders})


def success(request):
    if request.method == 'POST':
        a = request.POST
        print(a)
























