import os
from pymongo import AsyncMongoClient
from config.config import app_settings
import logging

db_client: AsyncMongoClient = None

async def get_db():
    db_name = app_settings.get('mongo_db')

    try:
        db = db_client.get_database(db_name)
        return db
    except Exception as e:
        logging.exception(f'Could not get database: {e}')
        raise

async def connect_and_init_db():
    global db_client
    
    host = app_settings.get('mongo_host')
    port = app_settings.get('mongo_port')
    user = app_settings.get('mongo_user')
    password = app_settings.get('mongo_password')
    mongo_uri = f'mongodb://{user}:{password}@{host}:{port}'
    
    try:
        db_client = AsyncMongoClient(mongo_uri)
        logging.info('Connected to mongo.')
    except Exception as e:
        logging.exception(f'Could not connect to mongo: {e}')
        raise

async def close_db_connect():
    global db_client
    if db_client is None:
        logging.warning('Connection is None, nothing to close.')
        return
    await db_client.close()
    db_client = None
    logging.info('Mongo connection closed.')