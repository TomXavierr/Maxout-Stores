# Generated by Django 4.1.6 on 2023-03-27 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_payment_order_alter_orders_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_id',
            field=models.CharField(default='803F69B7', max_length=8),
        ),
    ]
