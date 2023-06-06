# Generated by Django 4.0.5 on 2023-06-06 09:33

import django.core.validators
from django.db import migrations, models
import obcine.validators


class Migration(migrations.Migration):

    dependencies = [
        ('obcine', '0014_monthlyrevenue_created_at_monthlyrevenue_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlyexpensedocument',
            name='file',
            field=models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx']), obcine.validators.document_size_validator, obcine.validators.validate_expanse_file], verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='monthlyrevenuedocument',
            name='file',
            field=models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx']), obcine.validators.document_size_validator, obcine.validators.validate_revenue_file], verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='plannedexpensedocument',
            name='file',
            field=models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx']), obcine.validators.document_size_validator, obcine.validators.validate_expanse_file], verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='plannedrevenuedocument',
            name='file',
            field=models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx']), obcine.validators.document_size_validator, obcine.validators.validate_revenue_file], verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='yearlyexpensedocument',
            name='file',
            field=models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx']), obcine.validators.document_size_validator, obcine.validators.validate_expanse_file], verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='yearlyrevenuedocument',
            name='file',
            field=models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx']), obcine.validators.document_size_validator, obcine.validators.validate_revenue_file], verbose_name='File'),
        ),
    ]
