# Generated by Django 3.2.4 on 2021-08-19 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_service_companion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='duration',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='endpoint',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='price_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.pricetype'),
        ),
    ]