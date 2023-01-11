# Generated by Django 3.2.4 on 2023-01-11 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='singleproduct',
            name='price',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
