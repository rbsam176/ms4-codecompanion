# Generated by Django 3.2.4 on 2021-08-16 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0026_alter_companionprofile_bio'),
        ('services', '0008_remove_service_companion'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='companion',
            field=models.ManyToManyField(to='profiles.CompanionProfile'),
        ),
    ]
