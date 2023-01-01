from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi

from json_excel_api.dependencies import security, get_current_username

from .config import settings
from .routers import excel

app = FastAPI(dependencies=[Depends(get_current_username), Depends(security)], docs_url=settings.docs_url, redoc_url=settings.redoc_url)
#app.mount("/static", StaticFiles(directory="json_excel_api/static"), name="static")


# routers
app.include_router(excel.router)


# config swagger
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
