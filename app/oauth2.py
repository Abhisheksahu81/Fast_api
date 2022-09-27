
from jose import JWTError, jwt
from datetime import datetime , timedelta
from fastapi import Depends, status , HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings
oauth_scheme = OAuth2PasswordBearer(tokenUrl= 'login')

from app import schemas


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRATION_MINUTES = settings.access_token_expiration_minutes

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRATION_MINUTES) 
    to_encode.update({"expire" : f"{expire}"})

    to_encode = jwt.encode(to_encode , SECRET_KEY , algorithm = ALGORITHM)
    return to_encode

def verify_access_token(token : str , credential_exception):
    try:
        payload = jwt.decode(token , SECRET_KEY ,[ALGORITHM])
        id : str = payload.get("user_id")
        if not id : 
            raise credential_exception
        token_data = schemas.TokenData(id = id) 
    except JWTError:
        raise credential_exception
    return token_data    

def get_current_user(token : str = Depends(oauth_scheme)):
    credential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials" , headers = {"WWW-Authenticate" : "Bearer"})

    return verify_access_token(token, credential_exception=credential_exception)
