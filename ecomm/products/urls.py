from django.urls import path,include
from django.conf import settings
from .views import *
from .middlewares.auth import auth_middleware


urlpatterns = [
    path('product_details/<int:pk>/',ProductDetailsView.as_view(), name = 'product_details'),
    path('add_to_cart/<int:id>',AddToCartView.as_view(),name='add_to_cart'),
    path('cart/',CartView.as_view(),name='cart'),
    path('place_order/',CheckOutView.as_view(),name='place_order'),
    path('order_history/', auth_middleware(OrderHistoryView.as_view()),name='order_history'),
    path('minuscart/', minus_cart.as_view(),name='minuscart'),
    path('removecart/', RemoveCartItemView.as_view(),name='removecart'),
    path('productfilter/<str:id>',ProductFilterView.as_view(),name='productfilter'),
    path('search_product/', ProductSearchView.as_view(), name="search_product"),

    path('removewishlist/<int:pk>', RemoveWishlistView.as_view(), name="removewishlist"),
    path('trackorder/', TrackingOrderView.as_view(),name='trackorder'),
    # path('complete/', paymentcomplete, name="complete"),
    path('showwishlist/',showwishlist,name='showwishlist'),
    path('addwishlist/<int:id>/',addwishlist,name='addwishlist'),
    path('success', pay_success, name="pay_success"),
    path('cancel', pay_cancel, name="pay_cancel"),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path('PaymentDone/', PaymentDone, name="PaymentDone"),
    path('checkouts', create_checkout, name="checkouts"),

]

