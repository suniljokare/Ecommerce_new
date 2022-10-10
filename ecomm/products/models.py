from random import choices
from django.db import models
from base.models import BaseModel
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel, TreeForeignKey
from accounts.models import CustomUserModel

# Create your models here.



class Category(BaseModel,MPTTModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    status = models.BooleanField(default=False)

    parent = TreeForeignKey('self',blank=True, null=True, related_name='child', on_delete=models.CASCADE )

    class Meta:
        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"   

    def __str__(self):                           
        full_path = [self.name]            
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])


class Product(BaseModel):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=200)
    short_description = models.CharField(max_length=255)
    long_description = models.TextField(max_length=255)
    price = models.FloatField(max_length=255)
    special_price = models.FloatField(max_length=255)
    special_price_from = models.DateField(auto_now= True)
    special_price_to = models.DateField(auto_now= True)
    status = models.BooleanField(default=False)
    quantity = models.IntegerField()
    meta_title = models.TextField(max_length=100)
    meta_description = models.TextField(max_length=100)
    meta_keywords = models.TextField(max_length=100)
    category    = models.ForeignKey(
        'Category',
        related_name="products",
        on_delete=models.CASCADE
    ) 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return self.slug

    def __str__(self) -> str:
        return self.name
    # is_featured = models.BinaryField(default=0)


class ProductImages(BaseModel):
    image =  models.ImageField(upload_to="product")
    status = models.BooleanField(default=False)
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="product_images")

    class Meta:
        verbose_name_plural = "productimages"   


class WhishList(BaseModel):
    product  = models.CharField(max_length=255)



class Product_Attributes(BaseModel):
    name = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Product_attributes" 


    def __str__(self) -> str:
        return self.name


class Product_Attributes_Values(BaseModel):
    product_attribute = models.ForeignKey(Product_Attributes , on_delete=models.CASCADE , related_name="product_attributes_values")
    attribute_value = models.CharField(max_length=200, null=True, blank=True)


    class Meta:
        verbose_name_plural = "Product_attributes_values" 

    
    def __str__(self) -> str:
        return self.attribute_value


class Product_Attributes_Details(BaseModel):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="product_attributes_details")
    product_attribute = models.ForeignKey(Product_Attributes , on_delete=models.CASCADE , related_name="product_attributes_details")
    product_attribute_value = models.ForeignKey(Product_Attributes_Values , on_delete=models.CASCADE , related_name="product_attributes_details")


    class Meta:
        verbose_name_plural = "product_attributes_details" 
    
    def __str__(self) -> str:
        return self.product.name



class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    # percent_off = models.FloatField()
    discount_price  = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=100)
    no_of_uses = models.IntegerField(default=1)


    def __str__(self) -> str:
        return self.coupon_code





STATE_CHOICES = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),
("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),
("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),
("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),
("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),
("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),
("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),
("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),
("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),
("Puducherry","Puducherry"))


CITY_CHOICES =(('Pune','Pune'),('Mumbai','Mumbai'),('Delhi','Dehli'),('Chennai','Chennai'),('Banglore','Banglore'),('Siliguri','Siliguri'))


PAYMENT_CHOICES =(('wallet','wallet'),('card','card'),('netbanking','netbanking'),('emi','emi'),('paypal','paypal'),('cod','cod'))



class Order(BaseModel):
    user = models.ForeignKey(CustomUserModel , on_delete=models.CASCADE , related_name="order")
    payment_method= models.CharField(choices =PAYMENT_CHOICES, max_length=50, default='cod')
    # awb_no = models.CharField(max_length=200) 
    # payment = models.OneToOneField(PaymentGateway , on_delete=models.CASCADE , related_name="order")
    # transaction = 
    status = models.BooleanField(default=False)
    grand_total = models.FloatField(blank=True, null=True)
    shipping_charges =  models.FloatField()
    # coupon = models.OneToOneField(Coupon , on_delete=models.CASCADE , related_name="coupon_used")
    name = models.CharField(max_length=10) 
    mobile = models.CharField(max_length=10) 
    pincode = models.CharField(max_length=100) 
    locality = models.CharField(max_length=100) 
    address= models.CharField(max_length=1024) 
    city = models.CharField(choices=CITY_CHOICES, max_length =100) 
    state = models.CharField(choices=STATE_CHOICES, max_length =100) 
    landmark = models.CharField(max_length=100) 
    alternate_mobile = models.CharField(max_length=100) 


    def __str__(self) -> str:
        return self.name



class OrderDetails(BaseModel):
    order = models.ForeignKey(Order , on_delete=models.CASCADE , related_name="orderdetails")
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="orderdetails")
    quantity = models.IntegerField()
    amount = models.FloatField()


# class CouponsUsed(BaseModel):
#     user = models.OneToOneField(Profile , on_delete=models.CASCADE , related_name="coupon_used")
#     order = models.OneToOneField(Order , on_delete=models.CASCADE , related_name="coupon_used")
#     coupon = models.OneToOneField(Coupon , on_delete=models.CASCADE , related_name="coupon_used")

# class Category(BaseModel):
#     name = models.CharField(max_length=200)
#     # parent = models.IntegerField()
#     status = models.BooleanField(default=False)



# class ProductCategories(BaseModel):
#     category = models.OneToOneField(Category , on_delete=models.CASCADE , related_name="product_categories")
#     product = models.OneToOneField(Product , on_delete=models.CASCADE , related_name="product_categories")





































































































































































































































































































































































































































































































































































































































































































































































































































































































































