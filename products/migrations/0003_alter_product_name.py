# Generated by Django 3.2.4 on 2023-01-15 09:41

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.ForeignKey(default=uuid.uuid4, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='products.singleproduct'),
        ),
    ]
