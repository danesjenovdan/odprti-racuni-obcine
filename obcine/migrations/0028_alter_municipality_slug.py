# Generated by Django 4.0.5 on 2023-11-21 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obcine', '0027_municipality_slug_fill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipality',
            name='slug',
            field=models.SlugField(default='', unique=True, verbose_name='Slug'),
            preserve_default=False,
        ),
    ]