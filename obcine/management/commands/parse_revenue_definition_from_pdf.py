# -*- coding: utf-8 -*-
import pdfplumber
import requests
from django.core.management.base import BaseCommand

from obcine import models


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
    help = "Parse revenue definitions from PDF"

    def add_arguments(self, parser):
        parser.add_argument("pdf_url", type=str, help="PDF URL to parse")

    def handle(self, *args, **options):
        response = requests.get(options["pdf_url"])

        with open("files/kontni-nacrt.pdf", "wb") as f:
            f.write(response.content)

        order = models.RevenueDefinition.objects.all().order_by("-order")[0].order

        konti = []
        with pdfplumber.open("files/kontni-nacrt.pdf") as pdf:
            for page in pdf.pages:
                lines = page.extract_text().split("\n")
                state = "meta"
                text_buffer = ""
                code_buffer = ""

                for line in lines:

                    line = line.strip()
                    if not line:
                        continue
                    if state == "meta":
                        if line.startswith("Konto"):
                            state = "konti"
                        continue

                    if line.startswith("RAZRED"):
                        split_line = line.split(" ", 2)
                        fixed_line = [f"{split_line[0]} {split_line[1]}", split_line[2]]
                        konti.append(fixed_line)
                    elif line[0].isdigit() and not state == "multi_line_konto_name":
                        if "/" in line:
                            continue
                        if state == "multi_line_konto":
                            split_line = line.split(" ", 1)
                            code_buffer = split_line[0]
                            if len(split_line) > 1:
                                text_buffer += " " + split_line[1]
                            else:
                                state = "multi_line_konto_name"
                        elif state == "konti":
                            split_line = line.split(" ", 1)
                            konti.append(split_line)
                    else:
                        # multiline konto text
                        state = "multi_line_konto"
                        text_buffer += " " + line
                        if code_buffer:
                            konti.append([code_buffer, text_buffer.strip()])
                            code_buffer = ""
                            text_buffer = ""
                            state = "konti"

        for kont in konti:
            if kont[0][0] in ["5", "7"]:
                if len(kont) == 1:
                    print(
                        f"{bcolors.WARNING}Skipping {kont[0]} because title wasn't parsed.{bcolors.ENDC}"
                    )
                    continue
                code = kont[0].strip()
                title = kont[1].strip()
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
