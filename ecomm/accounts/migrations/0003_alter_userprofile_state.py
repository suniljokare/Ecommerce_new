# Generated by Django 3.2.16 on 2022-12-02 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20221108_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='state',
            field=models.CharField(choices=[('Maharashtra', 'Maharashtra'), ('Goa', 'Goa'), ('Gujrat', 'Gujrat')], max_length=50),
        ),
    ]
