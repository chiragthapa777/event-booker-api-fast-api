from contextlib import asynccontextmanager
import logging
import uvicorn
from fastapi import FastAPI
from app.core import config, logger
from app.core.aws.s3 import setup_s3
from app.core.database import close_db, setup_db
from app.core.exception_handler import setup_exception_handler
from app.enums.env_enum import Env
from app.middleware import setup_middleware
import app.routers as router


# setup config
config.setup_config()
conf = config.get_config()
logger.setup_logger()
log = logger.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info(f"Application started at port {conf.port}")

    # initialize DB
    setup_db(db_url=conf.db_url, echo_query=conf.echo_query)
    log.info("Database setup completed")

    setup_s3(conf=conf)

    yield

    log.info("Shutting down FastAPI application...")
    close_db()
    log.info("Closing database connection")


app = FastAPI(
    title=conf.app_name,
    debug=conf.debug,
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": True},
)
setup_exception_handler(app)
setup_middleware(app)

router.setup_router(app)

if __name__ == "__main__":
    log.info("Starting uvicorn server")
    uvicorn.run(
        "main:app",
        host=conf.host,
        port=conf.port,
        reload=conf.env == Env.LOCAL,
        log_config=None,
    )
