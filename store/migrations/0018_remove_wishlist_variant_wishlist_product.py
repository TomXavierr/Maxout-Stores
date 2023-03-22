# Generated by Django 4.1.6 on 2023-03-16 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_coupons_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='variant',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.products'),
            preserve_default=False,
        ),
    ]
