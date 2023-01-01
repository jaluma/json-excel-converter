from fastapi import APIRouter
from fastapi.responses import FileResponse

from json_excel_api.models.model import ExcelRequest
from json_excel_api.utils import random_name, map_format

from json_excel_converter import Converter
from json_excel_converter.xlsx import DEFAULT_COLUMN_WIDTH, DEFAULT_ROW_HEIGHT, Writer

router = APIRouter(prefix="/excel",
                   tags=["excel"],
                   responses={400: {"description": "Bad request"}, 404: {"description": "Not found"}})


@router.post("/")
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
                   global_configs=(model.global_settings or {}).__dict__,
                   start_row=worksheet.start_row,
                   start_col=worksheet.start_column
                )

        conv = Converter()
        conv.convert(worksheet.data, w)

        if not workbook:
            workbook = w.workbook

    workbook.close()

    headers = {f'Content-Disposition': f'attachment; filename="{model.filename}.xlsx"'}
    return FileResponse(excel_file_path, headers=headers)