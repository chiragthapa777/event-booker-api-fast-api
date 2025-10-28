import jwt
from datetime import datetime, timedelta, timezone

from app.core.config import get_config
from app.types import ErrStr
from app.utils import is_valid_uuid

ALGORITHM = "HS256"


def create_access_token(user_id: str, expires_in_minutes: int = 30, secret_key=str) -> str:
    """
    Create a JWT token containing user_id and expiry.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, secret_key, algorithm=ALGORITHM)
    return token


def verify_token(token: str, secret_key:str) -> dict:
    """
    Verify a JWT token and return the decoded payload.
    Raises jwt exceptions if invalid or expired.
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload  # payload contains 'sub' (user_id), 'exp', 'iat'
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")


def verify_extract_user_id(token: str) -> tuple[str,bool,ErrStr]:
    """
    Extract user_id ('sub' claim) from the token after verification.
    """
    try:
        payload = verify_token(token, get_config().access_token_secret)
        user_id = payload.get("sub")
        if not is_valid_uuid(user_id):
            raise Exception("invalid user id in token")
        return user_id, True, ""
        
    except Exception as e:
        return "", False, str(e)
