from django.urls import path
from .views import *
urlpatterns = [
    path('',HomePageView.as_view(),name='homepage'),
    path('products', HomeView.as_view(), name='products'),

]
