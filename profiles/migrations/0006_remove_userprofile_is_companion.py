# Generated by Django 3.2.4 on 2021-06-22 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_userprofile_is_companion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_companion',
        ),
    ]
