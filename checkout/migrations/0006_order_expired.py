# Generated by Django 3.2.4 on 2021-07-18 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_order_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='expired',
            field=models.BooleanField(default=False),
        ),
    ]