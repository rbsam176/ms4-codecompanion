# Generated by Django 3.2.4 on 2021-08-19 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0010_order_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='notes',
            field=models.TextField(default=''),
        ),
    ]