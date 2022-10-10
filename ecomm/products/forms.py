from django import forms
from .models import *


class AddressForm(forms.ModelForm):
    class Meta:
        model = Order
        fields= ['name','mobile','pincode','locality','address','city','state','landmark','alternate_mobile']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
        'mobile':forms.TextInput(attrs={'class':'form-control'}),
        'pincode':forms.NumberInput(attrs={'class':'form-control'}),
        'locality':forms.TextInput(attrs={'class':'form-control'}),
        'address':forms.TextInput(attrs={'class':'form-control'}),
        'city':forms.Select(attrs={'class':'form-control'}),
        'state':forms.Select(attrs={'class':'form-control'}),
        'landmark':forms.TextInput(attrs={'class':'form-control'}),
        'alternate_mobile':forms.TextInput(attrs={'class':'form-control'}),
        }



 