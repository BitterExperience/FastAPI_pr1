
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta


from app.core.config_db import setting


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expiration = datetime.now(timezone.utc) + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiration})
    return jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)

def decode_access_token(token: str) -> D:
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        return payload
    except JWTError:
        return None
