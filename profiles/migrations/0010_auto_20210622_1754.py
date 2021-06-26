# Generated by Django 3.2.4 on 2021-06-22 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_userprofile_is_companion'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='friday_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='monday_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='thursday_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='tuesday_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='wednesday_available',
            field=models.BooleanField(default=False),
        ),
    ]