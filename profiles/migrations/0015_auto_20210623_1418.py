# Generated by Django 3.2.4 on 2021-06-23 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_alter_availability_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availability',
            name='day',
        ),
        migrations.AddField(
            model_name='availability',
            name='friday_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='availability',
            name='monday_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='availability',
            name='thursday_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='availability',
            name='tuesday_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='availability',
            name='wednesday_available',
            field=models.BooleanField(default=False),
        ),
    ]