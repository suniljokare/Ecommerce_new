from django.db import models

# Create your models here.


class BannerSlider(models.Model):
    DISCOUNT_DEALS = (
    ('HOT DEALS', 'HOT DEALS'),
    ('New Arrivals','New Arrivals'),
)
    Image = models.ImageField(upload_to="product")
    Discount_Deals = models.CharField(choices=DISCOUNT_DEALS, max_length =255)
    Title = models.CharField(max_length=255)
    Description = models.CharField(max_length=255)
    Price_tag_Image = models.ImageField(upload_to="product", null=True, blank=True)

    def __str__(self):
        return self.Title
    