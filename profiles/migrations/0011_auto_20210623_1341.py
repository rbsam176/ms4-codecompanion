# Generated by Django 3.2.4 on 2021-06-23 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20210622_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email_address',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_name',
        ),
    ]
