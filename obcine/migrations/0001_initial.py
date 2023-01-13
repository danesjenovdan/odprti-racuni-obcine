# Generated by Django 4.0.5 on 2023-01-05 16:11

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields
import obcine.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Name')),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(verbose_name='End date')),
            ],
            options={
                'verbose_name': 'Financial year',
                'verbose_name_plural': 'Financial years',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.TextField(verbose_name='Nemo of municipality')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MunicipalityFinancialYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('financial_year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='obcine.financialyear')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='obcine.municipality')),
            ],
        ),
        migrations.CreateModel(
            name='RevenueDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('code', models.TextField(verbose_name='Code')),
                ('order', models.IntegerField(verbose_name='Order')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories_children', to='obcine.revenuedefinition', verbose_name='Parent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlannedRevenueDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx']), obcine.models.document_size_validator], verbose_name='File')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revenue_documents', to='obcine.municipality', verbose_name='Municipality')),
                ('municipality_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revenue_documents', to='obcine.municipalityfinancialyear', verbose_name='Municipality Financial Year')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revenue_documents', to='obcine.financialyear', verbose_name='Year')),
            ],
            options={
                'verbose_name': 'Planned revenue document',
                'verbose_name_plural': 'Planned revenue documents',
                'unique_together': {('municipality', 'year')},
            },
        ),
        migrations.CreateModel(
            name='PlannedRevenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('code', models.TextField(verbose_name='Code')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Amount')),
                ('definition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='obcine.revenuedefinition', verbose_name='RevenueDefinition')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obcine.plannedrevenuedocument')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='obcine.municipality', verbose_name='Organiaztion')),
                ('year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='obcine.financialyear', verbose_name='Year')),
            ],
        ),
        migrations.CreateModel(
            name='PlannedExpenseDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx']), obcine.models.document_size_validator], verbose_name='File')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_documents', to='obcine.municipality', verbose_name='Municipality')),
                ('municipality_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_documents', to='obcine.municipalityfinancialyear', verbose_name='Municipality Financial Year')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_documents', to='obcine.financialyear', verbose_name='Year')),
            ],
            options={
                'verbose_name': 'Planned expense document',
                'verbose_name_plural': 'Planned expense documents',
                'unique_together': {('municipality', 'year')},
            },
        ),
        migrations.CreateModel(
            name='PlannedExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Amount')),
                ('order', models.IntegerField(verbose_name='Order')),
                ('instructions', models.TextField(verbose_name='Instructions')),
                ('code', models.TextField(verbose_name='Code')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obcine.plannedexpensedocument')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='obcine.municipality', verbose_name='Organiaztion')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories_children', to='obcine.plannedexpense', verbose_name='Parent')),
                ('year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='obcine.financialyear', verbose_name='Year')),
            ],
            options={
                'verbose_name': 'Planned expense',
                'verbose_name_plural': 'Planned expense',
            },
        ),
        migrations.CreateModel(
            name='MonthlyRevenueDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx']), obcine.models.document_size_validator], verbose_name='File')),
                ('month', models.IntegerField(choices=[(1, 'Januar'), (2, 'Februar'), (3, 'Marec'), (4, 'April'), (5, 'Maj'), (6, 'Junij'), (7, 'Julij'), (8, 'Avgust'), (9, 'September'), (10, 'Oktober'), (11, 'November'), (12, 'December')], verbose_name='Month')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_revenue_documents', to='obcine.municipality', verbose_name='Municipality')),
                ('municipality_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_revenue_documents', to='obcine.municipalityfinancialyear', verbose_name='Municipality Financial Year')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_revenue_documents', to='obcine.financialyear', verbose_name='Year')),
            ],
            options={
                'verbose_name': 'Monthly revenue realization document',
                'verbose_name_plural': 'Monthly revenue realization documents',
                'unique_together': {('municipality', 'year', 'month')},
            },
        ),
        migrations.CreateModel(
            name='MonthlyRevenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('code', models.TextField(verbose_name='Code')),
                ('month', models.IntegerField(choices=[(1, 'Januar'), (2, 'Februar'), (3, 'Marec'), (4, 'April'), (5, 'Maj'), (6, 'Junij'), (7, 'Julij'), (8, 'Avgust'), (9, 'September'), (10, 'Oktober'), (11, 'November'), (12, 'December')], verbose_name='Month')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Amount')),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='obcine.revenuedefinition', verbose_name='RevenueDefinition')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obcine.monthlyrevenuedocument')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_revenue_realizations', to='obcine.municipality', verbose_name='Organiaztion')),
                ('year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='monthly_revenue_realizations', to='obcine.financialyear', verbose_name='Year')),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyExpenseDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx']), obcine.models.document_size_validator], verbose_name='File')),
                ('month', models.IntegerField(choices=[(1, 'Januar'), (2, 'Februar'), (3, 'Marec'), (4, 'April'), (5, 'Maj'), (6, 'Junij'), (7, 'Julij'), (8, 'Avgust'), (9, 'September'), (10, 'Oktober'), (11, 'November'), (12, 'December')], verbose_name='Month')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_expense_documents', to='obcine.municipality', verbose_name='Municipality')),
                ('municipality_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_expense_documents', to='obcine.municipalityfinancialyear', verbose_name='Municipality Financial Year')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_expense_documents', to='obcine.financialyear', verbose_name='Year')),
            ],
            options={
                'verbose_name': 'Monthly expense realization document',
                'verbose_name_plural': 'Monthly expense realization documents',
                'unique_together': {('municipality', 'year', 'month')},
            },
        ),
        migrations.CreateModel(
            name='MonthlyExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Amount')),
                ('order', models.IntegerField(verbose_name='Order')),
                ('instructions', models.TextField(verbose_name='Instructions')),
                ('code', models.TextField(verbose_name='Code')),
                ('month', models.IntegerField(choices=[(1, 'Januar'), (2, 'Februar'), (3, 'Marec'), (4, 'April'), (5, 'Maj'), (6, 'Junij'), (7, 'Julij'), (8, 'Avgust'), (9, 'September'), (10, 'Oktober'), (11, 'November'), (12, 'December')], verbose_name='Month')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obcine.monthlyexpensedocument')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='obcine.municipality', verbose_name='Organiaztion')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories_children', to='obcine.monthlyexpense', verbose_name='Parent')),
                ('year', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_related', to='obcine.financialyear', verbose_name='Year')),
            ],
            options={
                'verbose_name': 'Monthly expense',
                'verbose_name_plural': 'Monthly expense',
            },
        ),
        migrations.CreateModel(
            name='ExpenseDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Amount')),
                ('order', models.IntegerField(verbose_name='Order')),
                ('instructions', models.TextField(verbose_name='Instructions')),
                ('code', models.TextField(verbose_name='Code')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories_children', to='obcine.expensedefinition', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'Revenue definition',
                'verbose_name_plural': 'Revenue definitions',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('municipality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='obcine.municipality', verbose_name='Municipality')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
