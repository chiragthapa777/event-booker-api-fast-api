

from logging import Logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.http_logger import HTTPLoggerMiddleware



def setup_middleware(app:FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(middleware_class=HTTPLoggerMiddleware)