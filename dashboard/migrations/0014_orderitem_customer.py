# Generated by Django 3.2.7 on 2021-09-09 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_auto_20210909_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.customer'),
        ),
    ]
