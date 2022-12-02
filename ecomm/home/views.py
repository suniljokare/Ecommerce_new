from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponseRedirect
from products.models import *
from django.template.defaulttags import register
from django.views.generic import ListView, DetailView, View
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin



class HomePageView(TemplateView):
    template_name = "home/index.html"
    model = Product

    def get_context_data(self, **kwargs):
        # user = self.request.user or None
        # carts = Cart.usercart.for_user(user) 
        context = super().get_context_data(**kwargs)
        context = {
          'banners' :  BannerSlider.objects.all(),
           'cats' : Category.objects.filter(parent=None),
         'object_list' : Product.objects.all(),
        }
       
        return context


# class CategoryMixin(object):
#     def get_context_data(self, **kwargs):
#         context['cats'] = Category.objects.filter(parent=None),
#         context['banners'] = BannerSlider.objects.all(),
#         return context


# class HomePageView(CategoryMixin,ListView):
#     template_name = "home/index.html"
#     model = Product
#     paginate_by = 2
#     ordering = ['-name']


#     def get_context_data(self, **kwargs):
#         # user = self.request.user or None
#         # carts = Cart.usercart.for_user(user) 
#         print('!!!!!!!!!!!!!!!!!!!!!!!!!!1')
#         context = super(HomePageView,self).get_context_data(**kwargs)
#         # context = {
#         #   'banners' :  BannerSlider.objects.all(),
#         #    'cats' : Category.objects.filter(parent=None),
#         #  'object_list' : Product.objects.all(),
#         # }
       
#         return context


class HomeView(ListView):
    model = Product
    paginate_by = 2
    template_name: str = 'accounts/product_list.html'

    def get_context_data(self,**kwargs):
        context = super(HomeView,self).get_context_data(**kwargs)
        context['cats'] = Category.objects.filter(parent=None)
        return context


@register.filter
def get_range(value):
    return range(value)


