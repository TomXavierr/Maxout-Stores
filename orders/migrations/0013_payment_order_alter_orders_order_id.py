# Generated by Django 4.1.6 on 2023-03-27 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_alter_orders_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, to='orders.orders'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_id',
            field=models.CharField(default='5CC34C85', max_length=8),
        ),
    ]
