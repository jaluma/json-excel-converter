from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from json_excel_api.config import Settings

from json_excel_converter import Converter 
from json_excel_converter.xlsx import DEFAULT_COLUMN_WIDTH, DEFAULT_ROW_HEIGHT, Writer
from json_excel_converter.xlsx.formats import FontColor, LastUnderlined, Bold, \
    Centered, Format

import random
import string

app = FastAPI(docs_url=Settings.docs_url, redoc_url=Settings.redoc_url)
app.mount("/static", StaticFiles(directory="json_excel_api/static"), name="static")

@app.get("/")
def index():
    return {"Hello": "World"}

@app.post("/")
def create_item():
    excel_file_path = f'/tmp/{random_name(16)}.xlsx'
    w = Writer(excel_file_path,
            header_formats=(
               Centered,
               Bold,
               LastUnderlined,
               #FontColor('red')
            ),
            data_formats=(
               #FontColor('black'),
            ),
            column_widths={
                DEFAULT_COLUMN_WIDTH: 20
            },
            row_heights={
                DEFAULT_ROW_HEIGHT: 20
            }
        )

    data = [
        {'a': 'Hello'},
        {'a': 'World'}
    ]

    conv = Converter()
    conv.convert(data, w)

    headers = {'Content-Disposition': 'attachment; filename="Book.xlsx"'}
    return FileResponse(excel_file_path, headers=headers)

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