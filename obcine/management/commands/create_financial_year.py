from datetime import date

from django.core.management.base import BaseCommand

from obcine import models


class Command(BaseCommand):
    help = "Create financial year if it does not exist"

    def handle(self, *args, **options):
        current_year = date.today().year
        for i in range(4):
            create_year = current_year + i
            models.FinancialYear.objects.get_or_create(
                name=create_year,
                start_date=date(day=1, month=1, year=create_year),
                end_date=date(day=31, month=12, year=create_year),
            )
