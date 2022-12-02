from django.views.decorators.http import require_http_methods
from django.conf import settings    
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import *
from .templatetags.cart import *
from django.contrib import messages
from .forms import *
from django.db.models import Q
from django.http import JsonResponse
import json
from accounts.models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, View
from django.views import View
from django.views.generic.edit import UpdateView,DeleteView
from django.views.generic.base import TemplateView
import stripe
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os
import braintree
import datetime
from datetime import datetime, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save
from base.helper import send_emails
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from home.models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from base.helper import *
from django.core.paginator import Paginator
from django_filters.views import FilterView


######################### Product ############################


class ProductDetailsView(DetailView):
    model = Product


# class ProductSearchView(ListView):
#     model = Product
#     template_name = 'accounts/product_list.html'
#     paginate_by = 1

#     def get_queryset(self, **kwargs):
#         query = self.request.GET.get('search','')
#         return Product.objects.search(query)



class ProductSearchView(FilterView):
    template_name = 'accounts/product_list.html'
    model = Product
    context_object_name = "product"
    # filterset_class = StudentFilter
    paginate_by = 1 # Change as per your preference
    
    def get_queryset(self):
        query = self.request.GET.get('search','')
        return Product.objects.search(query)
        # organisation = self.request.user.userprofile
        # return Lead.objects.filter(organisation=organisation).order_by('first_name')


class ProductFilterView(View):

    def get(self, request, id):
        cats = Category.objects.filter(parent=None)
        products = Product.objects.filter(category_id=id)
        banners = BannerSlider.objects.all()
        context = {'object_list':products, 'cats':cats, 'banners':banners}
        return render(request, 'home/index.html', context)
       

######################## CART FUNCTIONALITY #########################################


class AddToCartView(LoginRequiredMixin,View):

   def get(self,request,id): 
        product= Product.objects.get(id=id)
        product_in_cart =Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        if not product_in_cart:
            cart =Cart(user=self.request.user,product=product)
            cart.save()
            # WishList.objects.get(product =product).delete()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class RemoveCartItemView(View):
    def get(self,request):
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        carts=Cart.obj(request.user)
        c.delete()
        data={
             'total':price_total(c),
             'total_amount' :total_cart_price(carts)
            }
        return JsonResponse(data)


class minus_cart(View):
    def get(self,request): 
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(product=prod_id,user=request.user)
        if request.GET.get('op') =='minus':
            if c.quantity >1 :
                c.quantity -= 1
                c.save()
        else:
            c.quantity += 1
            c.save()

        carts=Cart.obj(request.user)
        total=price_total(c),
        total_amount =total_cart_price(carts)
        data={
                    'quantity':c.quantity,
                    'total':total,
                    'total_amount':total_amount
                }
        return JsonResponse(data)


class CartView(LoginRequiredMixin,View):

    def get(self,request): 
        carts = Cart.obj(request.user)
        total = total_cart_price(carts)
        request.session['total'] = total
        context = {'carts':carts,'total':total}
        return render(request,'products/cart.html', context)


    def post(self,request): 
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
        carts = Cart.obj(request.user)

        if not coupon_obj.exists():
            messages.warning(request, 'Invalid Coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if total_cart_price(carts) < coupon_obj[0].minimum_amount:
            messages.warning(request, f'amount should be greater than {coupon_obj[0].minimum_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj[0].is_expired:
            messages.warning(request, f'coupon expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        total = total_cart_price(carts, coupon_obj[0])
        coupon_obj.update(is_expired = True)
        coupon_obj[0].save()

        request.session['total'] = total
        messages.success(request, 'Coupon applied')

        return render(request, 'products/cart.html', {'total':total, 'carts':carts})


@method_decorator(csrf_exempt, name='dispatch')
class CheckOutView(View):
    payment_methods = PaymentGateway.objects.all()
    
    def get(self,request,*args):
        userinfo = get_or_none(CustomUserModel, id=request.user.id)
        adress = get_or_none(UserProfile, user=request.user,default=True)

        context =  {
                    'payment_methods':self.payment_methods,
                      'form':CheckoutForm(),
                      'userinfo':userinfo,
                      'adress':adress
                   }
        return render(self.request, 'products/checkout.html', context)
    
    
    def post(self,request,*args):
        form = CheckoutForm(request.POST)
        total = request.session.get('total')
        request.session['total'] = 0
        carts = Cart.obj(request.user)
        
        if form.is_valid():         
            fm = form.save(commit=False)
            fm.user =request.user
            fm.grand_total=total
            fm.save()
            order = (CustomerOrder.objects.filter(user=request.user,status =False)).last()

            # carts.delete()

            for cart in carts:
                orderdetails = OrderDetails(
                    order=order, product=cart.product, 
                    quantity=cart.quantity, amount=cart.product.price 
                    )
                orderdetails.save()
            
            if request.POST.get('payment_gateway') == '1':
                # order_placed_mail(order)
                return render(request, 'products/order_placed.html',{'order':order,'total':total})

            if request.POST.get('payment_gateway') == '2':
                client = razorpay.Client(auth = (settings.KEY_ID, settings.KEY_SECRET))                        
                payment = client.order.create( dict(amount =int(total)*100, 
                                                    currency = 'INR', 
                                                    payment_capture = 1))      
                
                context = {'client':client,'payment':payment,'razorpay_merchant_key':settings.KEY_ID}
                return render(request, 'products/razorpay.html',context)

            if request.POST.get('payment_gateway') == '3':
                return render(request, 'products/paypal.html',{'total':total} )

            if request.POST.get('payment_gateway') == '4':
                return redirect ("create-checkout-session") 

            if request.POST.get('payment_gateway') == '5':
                context = {'client_token' : str(generate_client_token()),'total':total}
                return render(request, 'products/braintree.html', context)

        context = {'payment_methods' :self.payment_methods,'form':form}

        return render(self.request, 'products/checkout.html', context)
        

def razorpaycheck(request):
    carts = Cart.obj(request.user)
    total = total_cart_price(carts)
    
    return JsonResponse({
        ''
    })


@csrf_exempt
@require_http_methods(['POST'])
def PaymentDone(request):
    try:
        transaction=request.POST.get('razorpay_payment_id')
        fm =CustomerOrder.objects.filter(status=False).last()
        fm.transaction_id=transaction
        fm.status=True
        fm.save()
        order_placed_mail(fm)
        return render(request, 'products/order_placed.html', {'order':fm})

    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      

####################### Order Management ##################################    

class OrderHistoryView(TemplateView):
    template_name = 'products/order_history.html'
    def get_context_data(self,*args, **kwargs):
        context = super(OrderHistoryView, self).get_context_data(*args,**kwargs)
        context['orders'] = OrderDetails.objects.filter(order__user=self.request.user)
        return context


class TrackingOrderView(TemplateView):
    template_name = 'products/trackorder.html'

    def post(self,*args,**kwargs):
        awb = self.request.POST.get('awb')
        updates = OrderDetails.objects.filter(order__awb_no =str(awb),order__user=self.request.user)
        return super(TemplateView, self).render_to_response({'updates':updates})


##########################  WHISHLIST ######################################

def addwishlist(request,id=None):
    product = Product.objects.get(id=id)
    user = request.user
    
    a = WishList.obj(product.id,request.user).exists()
    product_already_in_wishlist = a
    if product_already_in_wishlist:
        pass
    else:
        WishList(user=user,product=product).save()
    return redirect(showwishlist)


@login_required(login_url='login')
def showwishlist(request):
    user = request.user
    products = WishList.objects.filter(user=user)
    wishlist_product = [ p for p in WishList.objects.all() if p.user == user]
    if wishlist_product:
        return render(request,'products/wishlist.html',{'products':products})
    else:
        return render(request,'products/emptywishlist.html')


class RemoveWishlistView(View):
    def get(self,request,pk):
        remove_item = WishList.obj(pk,request.user)
        remove_item.delete()
        return render(request,'products/wishlist.html')

# class RemoveWishlistView(LoginRequiredMixin, DeleteView):

#     model = WishList

#     def delete(self,id, *args, **kwargs):
#         print('************************')
#         remove_item = WishList.objects.get(Q(product=id) & Q(user=self.request.user))
#         remove_item.delete()
#         return render(self.request,'products/wishlist.html')


###################################### stripe payment functionality ###################################

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSessionView(View):
    def get(self,request,*args,**kwargs):

        host = 'http://127.0.0.1:8000'
        carts = Cart.obj(request.user)
        total = total_cart_price(carts)
        checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
         line_items=[
            {
            'price_data':{
                'currency':'inr',
                'unit_amount':int(total)*100,
                'product_data':{
                    'name':'T-shirt',
                    'name':123,
                },
            },
            'quantity':1,
         },
         ],
        mode = 'payment',
        success_url = f'{host}/products/success',
        cancel_url = f'{host}/products/cancel',
        )

        fm = CustomerOrder.objects.filter(status=False).last()
        fm.transaction_id=checkout_session.id
        fm.status=True
        fm.save()
        return redirect(checkout_session.url, code=303)


def pay_success(request):
    order = (CustomerOrder.objects.filter(user=request.user,status =True)).last()
    return render(request, 'products/order_placed.html', {'order':order})


def pay_cancel(request):
    return render(request, 'products/cancel.html')


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        if session.payment_status == 'paid':
            line_item = session.list_items(session.id, limit=1).data[0]
            order_id = line_item['description']
            # fulfill_order(order_id)
            fulfill_order(order_id) 

    return HttpResponse(status=200)


def fulfill_order(order_id):

    order = Order.objects.get(id=order_id)
    order.ordered = True
    order.orderDate = datetime.datetime.now()
    order.save()
    print("Fulfilling order") 


######################################  Braintree Payment Integration  ###############################


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
    
        merchant_id=settings.MERCHANT_ID,
        public_key=settings.PUBLIC_KEY,
        private_key=settings.PRIVATE_KEY
    )
)

# pass client_token to your front-end
def generate_client_token():
    return str(gateway.client_token.generate())

def transact(options):
    return gateway.transaction.sale(options)

def find_transaction(id):
    return gateway.transaction.find(id)


def fulfill_order(order_id):

    order = CustomerOrder.objects.get(id=order_id)
    order.ordered = True
    order.orderDate = datetime.datetime.now()
    order.save()
    print("Fulfilling order") 


def create_checkout(request):
    result = transact({
        'amount': request.POST.get('amount'),
        'payment_method_nonce': request.POST.get('payment_method_nonce'),
        'options': {
            "submit_for_settlement": True
        }
    })
    if result.is_success or result.transaction:
        fm =CustomerOrder.objects.get(status=False)
        fm.transaction_id = result.transaction.id
        fm.status=True
        fm.save()
        print(result.transaction.id, '**********************')
        order = (CustomerOrder.objects.filter(user=request.user,status =True)).last()
        return render(request, 'products/order_placed.html', {'order':order})
        # return redirect(url_for('tr_show',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: 
            print(f'Error: {x.code}: {x.message}')
        return render(request, 'products/braintree.html' )
        


def tr_refund(request,transaction_id):
    transaction = gateway.transaction.find(transaction_id)
    
    if transaction.status == 'settled' or transaction.status == 'settling':
        result = gateway.transaction.refund(transaction_id)
        if result.is_success:
            print("Transaction successfully refunded.")
        else:
            print(f"Could not refund, error: {result.errors.deep_errors}")        
    return redirect(request,'products/tr_show', {'transaction_id':transaction_id})



# Void a transaction
def tr_void(request,transaction_id):
    transaction = gateway.transaction.find(transaction_id)
    
    if transaction.status == 'authorized' or transaction.status == 'submitted_for_settlement' or transaction.status == ' settlement_pending':
        result = gateway.transaction.void(transaction_id)
        if result.is_success:
            print("Transaction successfully voided.")
        else:
            print(f"Could not void the transaction, error: {result.errors.deep_errors}")
    return render(request,'products/tr_show', {'transaction_id':transaction_id})



