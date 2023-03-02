# Generated by Django 4.1.6 on 2023-03-01 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_delete_color_variants_variant_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variants',
            name='variant_sport',
        ),
        migrations.AddField(
            model_name='products',
            name='product_sport',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='store.sport'),
        ),
    ]
