# Generated by Django 4.1.6 on 2023-03-26 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_orders_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_id',
            field=models.CharField(default='B7500F4D', max_length=8),
        ),
    ]