from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config.settings import settings
from app.middleware.exception_handlers import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.routers.router import api_router

app = FastAPI(title="Todo API")

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Welcome to Todo API"}
