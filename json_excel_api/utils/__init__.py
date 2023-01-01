import random
import string

from json_excel_api.models.model import ExcelFormatDefinition, ExcelHeaderInfoDefinition
from json_excel_converter.xlsx.formats import Format


def map_format(header: ExcelFormatDefinition):
    if header is None:
        return

    return Format({
        header.key: header.value
    })


def map_column_config(header: ExcelHeaderInfoDefinition):
    if header is None:
        return

    return {
        header.name: header.column_width
    }


def random_name(length: int):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))