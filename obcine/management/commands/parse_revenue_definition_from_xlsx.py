# -*- coding: utf-8 -*-
from io import BytesIO

import openpyxl
import openpyxl.workbook.workbook
import openpyxl.worksheet.worksheet
import requests
import xlrd
from django.core.management.base import BaseCommand

from obcine import models
from obcine.parse_utils import (
    get_num_rows,
    get_row,
    get_row_values,
    get_sheet_by_index,
    open_workbook,
)


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Command(BaseCommand):
    help = "Parse revenue definitions from XLSX"

    def add_arguments(self, parser):
        parser.add_argument(
            "url", type=str, nargs="?", help="XLSX URL to parse (optional)"
        )

    def handle(self, *args, **options):
        if options.get("url"):
            response = requests.get(options["url"])

            with open("files/enotni-kontni-nacrt.xlsx", "wb") as f:
                f.write(response.content)

        order = models.RevenueDefinition.objects.all().order_by("-order")[0].order

        konti = []
        book = open_workbook("files/enotni-kontni-nacrt.xlsx")
        sheet = get_sheet_by_index(book, 0)
        for row_i in range(get_num_rows(sheet)):
            if row_i < 2:
                continue

            row = get_row(sheet, row_i)
            code = str(row[0].value)
            title = row[1].value.strip()

            if code[0] in ["5", "7"]:
                if len(code) < 2:
                    continue

                if code.startswith("5"):
                    if not code.startswith("50"):
                        continue

                revenue_definition = models.RevenueDefinition.objects.filter(
                    code=code,
                )
                if revenue_definition:
                    revenue_definition = revenue_definition[0]
                    if revenue_definition.name.strip().lower() != title.lower():
                        print(
                            f"Renaming [{code}] \n{bcolors.WARNING}{revenue_definition.name}{bcolors.ENDC} \n{bcolors.OKGREEN}{title}{bcolors.ENDC}\n"
                        )
                        revenue_definition.name = title
                        revenue_definition.save()

                else:
                    print(
                        f"Adding new revenue definition [{code}] {bcolors.OKGREEN}{title}{bcolors.ENDC}"
                    )

                    order += 1
                    parent_code = self.get_parent_code(code)
                    parent = models.RevenueDefinition.objects.filter(
                        code=parent_code
                    ).first()
                    revenue_definition = models.RevenueDefinition.objects.create(
                        code=code, name=title, order=order, parent=parent
                    )

        self.reorder_revenue_definitions()

    def get_parent_code(self, code):
        if len(code) == 6:
            return code[:4]
        elif len(code) == 4:
            return code[:3]
        elif len(code) == 3:
            return code[:2]

    def reorder_revenue_definitions(self):
        revenue_definitions = models.RevenueDefinition.objects.all()
        order = 1
        for revenue_definition in revenue_definitions:
            revenue_definition.order = order
            revenue_definition.save()
            order += 1
            order += 1
        order = 1
        for revenue_definition in revenue_definitions:
            revenue_definition.order = order
            revenue_definition.save()
            order += 1
            order += 1
