# Generated by Django 3.2.7 on 2021-09-09 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_orderitem_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.customer'),
        ),
    ]
