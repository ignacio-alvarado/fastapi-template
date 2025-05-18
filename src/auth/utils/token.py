from jwt import encode, decode
from datetime import datetime, timedelta, timezone
from config.config import app_settings

def create_token(user_id: str, role: str = None) -> dict:
    """
    Create a JWT access and refresh token for a user.
    
    Args:
        user_id (str): The ID of the user to create a token for.
        role (str, optional): The role of the user.

    Returns:    
        dict: The JWT token and refresh token.
    """
    access_payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=app_settings.get('jwt_expiration_minutes'))
    }

    refresh_payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(days=app_settings.get('jwt_refresh_expiration_days'))
    }

    return {
        "access_token": encode(
            access_payload,
            app_settings.get('jwt_secret'),
            algorithm=app_settings.get('jwt_algorithm')
        ),
        "refresh_token": encode(
            refresh_payload,
            app_settings.get('jwt_secret'),
            algorithm=app_settings.get('jwt_algorithm')
        )
    }

def create_activation_token(user_id: str) -> dict:
    """
    Create a JWT activation token for a user.

    Args:
        user_id (str): The ID of the user to create a token for.

    Returns:
        dict: The JWT token.
    """
    return encode(
        {"sub": str(user_id), "type": "activation"},
        app_settings.get('jwt_secret'),
        algorithm=app_settings.get('jwt_algorithm')
    )

def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.

    Args:
        token (str): The JWT token to verify and decode.

    Returns:
        dict: The decoded payload of the token.
    """
    return decode(
        token,
        app_settings.get('jwt_secret'),
        algorithms=[app_settings.get('jwt_algorithm')]
    )