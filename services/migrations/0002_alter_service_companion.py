# Generated by Django 3.2.4 on 2021-08-26 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='companion',
            field=models.ManyToManyField(blank=True, null=True, to='profiles.CompanionProfile'),
        ),
    ]