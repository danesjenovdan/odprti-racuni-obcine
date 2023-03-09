# Generated by Django 4.0.5 on 2023-03-08 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obcine', '0002_alter_monthlyexpensedocument_municipality_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('started_at', models.DateTimeField(blank=True, default=None, help_text='time when started', null=True)),
                ('finished_at', models.DateTimeField(blank=True, default=None, help_text='time when finished', null=True)),
                ('errored_at', models.DateTimeField(blank=True, default=None, help_text='time when errored', null=True)),
                ('error_msg', models.TextField()),
                ('name', models.TextField(help_text='Name of task')),
                ('email_msg', models.TextField(help_text='A message sent to the administrator when the task is complete.')),
                ('payload', models.JSONField(help_text='Payload kwargs')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
