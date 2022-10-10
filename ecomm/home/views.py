from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponseRedirect
from products.models import *

# Create your views here. 

# def home(request):
#     Banners = BannerSlider.objects.all()
#     context ={
#         'Banners': Banners
#     }
#     return render(request, 'home/index.html', context)

def home(request):      
    cats = Category.objects.filter(parent = None)  
    products = Product.objects.all()
    return render(request,'home/index.html',{'products':products,'cats':cats})