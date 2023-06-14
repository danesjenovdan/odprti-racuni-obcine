# Generated by Django 4.0.5 on 2023-06-13 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obcine', '0016_instructions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='municipalityfinancialyear',
            options={'verbose_name': 'Municipality financial year', 'verbose_name_plural': 'Municipality financial year'},
        ),
        migrations.AddField(
            model_name='monthlyexpense',
            name='timestamp',
            field=models.DateField(blank=True, null=True, verbose_name='Datum obdelave podatkov'),
        ),
        migrations.AddField(
            model_name='monthlyrevenue',
            name='timestamp',
            field=models.DateField(blank=True, null=True, verbose_name='Datum obdelave podatkov'),
        ),
    ]