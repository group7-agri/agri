# Generated by Django 3.2.4 on 2022-12-10 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_profile_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account',
            field=models.CharField(choices=[('Farmer', 'Farmer or Rancher'), ('Buyer', 'Merchant')], default='Farmer', max_length=200),
        ),
    ]
