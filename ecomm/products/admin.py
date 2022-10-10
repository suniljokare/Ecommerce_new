from django.contrib import admin
from .models import *
from mptt.admin import DraggableMPTTAdmin



# Register your models here.

# admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(WhishList)
admin.site.register(OrderDetails)

# admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','short_description','price','special_price','quantity','category' )


class CategorytAdmin(admin.ModelAdmin):
    list_display = ('name','slug' )



admin.site.register(Product,ProductAdmin)
admin.site.register(Category,DraggableMPTTAdmin)
admin.site.register(Product_Attributes)
admin.site.register(Product_Attributes_Values)
admin.site.register(Product_Attributes_Details)
admin.site.register(Coupon)
admin.site.register(Order)






# Register your models here.
