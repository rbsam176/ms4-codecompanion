# Generated by Django 3.2.4 on 2021-07-07 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0003_faqentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqentry',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='faq.faqcategory'),
        ),
        migrations.AlterField(
            model_name='faqentry',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='faqentry',
            name='title',
            field=models.CharField(max_length=254, null=True),
        ),
    ]
