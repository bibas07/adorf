# Generated by Django 3.2.6 on 2021-09-07 08:02

from django.db import migrations
import mirage.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='cardNum',
            field=mirage.fields.EncryptedIntegerField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='cname',
            field=mirage.fields.EncryptedCharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='cvv',
            field=mirage.fields.EncryptedIntegerField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='exd',
            field=mirage.fields.EncryptedCharField(max_length=200, null=True),
        ),
    ]
