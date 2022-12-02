from products.models import *

def extras(request):

    if request.user.is_authenticated:
       
        cart = Cart.objects.filter(user = request.user).count()
        cats = Category.objects.filter(parent=None)
        return {'cart':cart,'cats':cats}
    return {}