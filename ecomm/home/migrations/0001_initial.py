# Generated by Django 3.2 on 2022-10-02 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BannerSlider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='product')),
                ('Discount_Deals', models.CharField(choices=[('HOT DEALS', 'HOT DEALS'), ('New Arrivals', 'New Arrivals')], max_length=255)),
                ('Title', models.CharField(max_length=255)),
                ('Description', models.CharField(max_length=255)),
                ('Price_tag_Image', models.ImageField(blank=True, null=True, upload_to='product')),
            ],
        ),
    ]