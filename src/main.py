from fastapi import FastAPI, Request

from utils.logger import logger, init_logger
from config.db import connect_and_init_db, close_db_connect
from auth.routes import auth_router
from user.routes import user_router

app = FastAPI()

# Events
app.add_event_handler("startup", init_logger)
app.add_event_handler("startup", connect_and_init_db)
app.add_event_handler("shutdown", close_db_connect)

# Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

# Routes
app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/user")

