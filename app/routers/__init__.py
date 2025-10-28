

from fastapi import FastAPI

from app.routers import file_upload_router, user_router

from . import auth_router

def setup_router(app : FastAPI):
    app.include_router(auth_router.router)
    app.include_router(user_router.router)
    app.include_router(file_upload_router.router)