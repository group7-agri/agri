# Generated by Django 3.2.4 on 2023-01-20 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_order_productid'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='singleproduct',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
