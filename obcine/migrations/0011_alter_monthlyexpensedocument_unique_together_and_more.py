# Generated by Django 4.0.5 on 2023-05-11 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('obcine', '0010_municipality_financial_years_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='monthlyexpensedocument',
            unique_together={('municipality_year', 'month')},
        ),
        migrations.AlterUniqueTogether(
            name='monthlyrevenuedocument',
            unique_together={('municipality_year', 'month')},
        ),
        migrations.AlterUniqueTogether(
            name='plannedexpensedocument',
            unique_together={('municipality_year',)},
        ),
        migrations.AlterUniqueTogether(
            name='plannedrevenuedocument',
            unique_together={('municipality_year',)},
        ),
        migrations.AlterUniqueTogether(
            name='yearlyexpensedocument',
            unique_together={('municipality_year',)},
        ),
        migrations.AlterUniqueTogether(
            name='yearlyrevenuedocument',
            unique_together={('municipality_year',)},
        ),
    ]