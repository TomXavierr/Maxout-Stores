# Generated by Django 4.1.6 on 2023-03-03 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_image_variant_alter_image_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variants',
            name='variant_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='store.products'),
        ),
    ]
