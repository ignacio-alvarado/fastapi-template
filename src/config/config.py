import os
  
app_settings = {
    "mongo_host": os.getenv('NO_SQL_HOST', 'localhost'),
    "mongo_port": os.getenv('NO_SQL_PORT', 27017),
    "mongo_db": os.getenv('NO_SQL_DB', 'test'),
    "mongo_user": os.getenv('NO_SQL_USER', 'admin'),
    "mongo_password": os.getenv('NO_SQL_PASSWORD', 'password'),
    "jwt_secret": os.getenv('JWT_SECRET', 'secret'),
    "jwt_algorithm": os.getenv('JWT_ALGORITHM', 'HS256'),
    "jwt_expiration_minutes": int(os.getenv('JWT_EXPIRATION_MINUTES', 30)),
    "jwt_refresh_expiration_days": int(os.getenv('JWT_REFRESH_EXPIRATION_DAYS', 30)),
} 