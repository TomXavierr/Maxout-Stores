# Generated by Django 4.1.6 on 2023-02-15 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_account_is_blocked_alter_account_date_joined_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
