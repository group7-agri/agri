# Generated by Django 3.2.4 on 2023-01-15 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_order_productid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ProductId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='products.product'),
        ),
    ]
