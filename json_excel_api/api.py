from functools import reduce

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from json_excel_api.config import Settings
from json_excel_api.model import ExcelRequest, ExcelFormatDefinition, ExcelHeaderInfoDefinition

from json_excel_converter import Converter
from json_excel_converter.xlsx import DEFAULT_COLUMN_WIDTH, DEFAULT_ROW_HEIGHT, Writer
from json_excel_converter.xlsx.formats import LastUnderlined, Bold, \
    Centered, Format

import random
import string

app = FastAPI(docs_url=Settings.docs_url, redoc_url=Settings.redoc_url)
app.mount("/static", StaticFiles(directory="json_excel_api/static"), name="static")


@app.get("/")
def index():
    return {"Hello": "World"}


@app.post("/")
async def create_item(model: ExcelRequest):
    excel_file_path = f'/tmp/{random_name(16)}.xlsx'

    workbook = None
    for worksheet in model.data:
        w = Writer(excel_file_path,
                   workbook=workbook,
                   sheet_name=worksheet.name,
                   header_formats=[map_format(format_header) for format_header in
                                   filter(lambda x: x is not None, worksheet.definition.formats or [])],
                   data_formats=[map_format(format_data) for format_data in
                                 filter(lambda x: x is not None, worksheet.formats or [])],
                   column_widths=dict({DEFAULT_COLUMN_WIDTH: worksheet.definition.default_column_width}.items()
                                      | { header.name: header.column_width
                                          for header in filter(lambda x: x is not None, worksheet.definition.headers or []) }.items()
                                      ),
                   row_heights={
                       DEFAULT_ROW_HEIGHT: worksheet.definition.default_row_height
                   },
                   global_configs=(model.global_settings or {}).__dict__
                )

        conv = Converter()
        conv.convert(worksheet.data, w)

        if not workbook:
            workbook = w.workbook

    workbook.close()

    headers = {f'Content-Disposition': f'attachment; filename="{model.filename}.xlsx"'}
    return FileResponse(excel_file_path, headers=headers)


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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Freightol Excel SVC",
        version="2.0.0",
        description="Excel generator microservice",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
