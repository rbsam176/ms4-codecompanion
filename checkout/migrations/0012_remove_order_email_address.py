# Generated by Django 3.2.4 on 2021-08-19 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0011_alter_order_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='email_address',
        ),
    ]