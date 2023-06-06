# Generated by Django 4.0.5 on 2023-06-06 11:01

from django.db import migrations, models
import django.db.models.deletion
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('obcine', '0015_alter_monthlyexpensedocument_file_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instructions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_instructions', martor.models.MartorField(blank=True, null=True, verbose_name='Instructions for list of objects')),
                ('add_instructions', martor.models.MartorField(blank=True, null=True, verbose_name='Instructions for adding object')),
                ('edit_instructions', martor.models.MartorField(blank=True, null=True, verbose_name='Instructions for edit single object')),
                ('model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Instructions',
                'verbose_name_plural': 'Instructions',
            },
        ),
    ]
