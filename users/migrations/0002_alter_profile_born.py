# Generated by Django 3.2.4 on 2023-01-15 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='born',
            field=models.DateField(max_length=200, null=True, verbose_name='Date of Birth'),
        ),
    ]
