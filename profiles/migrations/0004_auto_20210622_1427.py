# Generated by Django 3.2.4 on 2021-06-22 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20210621_0731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='account_type',
        ),
        migrations.DeleteModel(
            name='AccountType',
        ),
    ]
