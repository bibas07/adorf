# Generated by Django 3.2.6 on 2021-08-28 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20210827_0908'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='area',
            new_name='phoneNum',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='phone',
            new_name='pickaddress',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='region',
            new_name='state',
        ),
    ]
