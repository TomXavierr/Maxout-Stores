# Generated by Django 4.1.6 on 2023-02-20 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_alter_addresses_mobile_alter_addresses_pincode'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos/'),
        ),
    ]
