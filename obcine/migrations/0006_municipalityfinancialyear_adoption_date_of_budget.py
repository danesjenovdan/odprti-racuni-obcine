# Generated by Django 4.0.5 on 2023-05-04 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("obcine", "0005_monthlyexpensedocument_created_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="municipalityfinancialyear",
            name="adoption_date_of_budget",
            field=models.DateField(
                default="2022-01-01", verbose_name="Datum sprejetja proračuna"
            ),
            preserve_default=False,
        ),
    ]
