# Generated by Django 3.2.4 on 2023-01-24 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_customuser_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='nid',
            field=models.PositiveIntegerField(blank=True, max_length=16, null=True),
        ),
    ]
