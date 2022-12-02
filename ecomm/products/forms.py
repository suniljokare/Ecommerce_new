from django import forms
from .models import *


# class AddressForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields= ['name','mobile','pincode','locality','address','city','state','landmark','alternate_mobile']
#         widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
#         'mobile':forms.TextInput(attrs={'class':'form-control'}),
#         'pincode':forms.NumberInput(attrs={'class':'form-control'}),
#         'locality':forms.TextInput(attrs={'class':'form-control'}),
#         'address':forms.TextInput(attrs={'class':'form-control'}),
#         'city':forms.Select(attrs={'class':'form-control'}),
#         'state':forms.Select(attrs={'class':'form-control'}),
#         'landmark':forms.TextInput(attrs={'class':'form-control'}),
#         'alternate_mobile':forms.TextInput(attrs={'class':'form-control'}),
#         }



class CheckoutForm(forms.ModelForm):
    class Meta:
        model = CustomerOrder
        fields= ['payment_gateway','name','mobile','email','billing_address_1','billing_address_2','billing_state','billing_city','billing_zipcode','shipping_address_1','shipping_address_2','shipping_city','shipping_state','shipping_zipcode']
      
       