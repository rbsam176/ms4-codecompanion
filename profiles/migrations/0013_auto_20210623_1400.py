# Generated by Django 3.2.4 on 2021-06-23 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_availability'),
    ]

    operations = [
        migrations.RenameField(
            model_name='availability',
            old_name='friday',
            new_name='day',
        ),
        migrations.RemoveField(
            model_name='availability',
            name='monday',
        ),
        migrations.RemoveField(
            model_name='availability',
            name='thursday',
        ),
        migrations.RemoveField(
            model_name='availability',
            name='tuesday',
        ),
        migrations.RemoveField(
            model_name='availability',
            name='wednesday',
        ),
    ]