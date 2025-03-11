import os

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from obcine.parse_utils import get_row_values, get_sheet_by_index, open_workbook


def document_size_validator(
    value,
):  # add this to some file where you can import it from
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(
            _("Datoteka je prevelika. Največja možna velikost je 10 MB.")
        )


def image_validator(image):
    limit = 1 * 1024 * 1024
    if image.size > limit:
        raise ValidationError(_("Slika je prevelika. Največja možna velikost je 1 MB."))


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [".jpg", ".jpeg", ".png"]
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            _("Format slike ni veljaven ali pa je slika poškodovana.")
        )


def validate_expanse_file(value):
    book = open_workbook(file_contents=value.read())
    sheet = get_sheet_by_index(book, 0)
    requierd_rows = [
        "PU_ID",
        "PU_OPIS",
        "PPP_ID",
        "PPP_OPIS",
        "GPR_ID",
        "GPR_OPIS",
        "PPR_ID",
        "PPR_OPIS",
        "PP_ID",
        "PP_OPIS",
        "K4_ID",
        "K4_OPIS",
        "BLC_ID",
        "BLC_OPIS",
        "F1",
        "F2",
        "F3",
    ]
    if get_row_values(sheet, 0) != requierd_rows:
        raise ValidationError(_("Datoteka ni pravilno izvozena iz sitema APRA."))


def validate_revenue_file(value):
    book = open_workbook(file_contents=value.read())
    sheet = get_sheet_by_index(book, 0)
    requierd_rows = ["BLC_ID", "K6_ID", "K6_OPIS", "VREDNOST_PRI"]
    if get_row_values(sheet, 0) != requierd_rows:
        raise ValidationError(_("Datoteka ni pravilno izvozena iz sitema APRA."))
