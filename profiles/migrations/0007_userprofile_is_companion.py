# Generated by Django 3.2.4 on 2021-06-22 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_remove_userprofile_is_companion'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_companion',
            field=models.BooleanField(default=False),
        ),
    ]