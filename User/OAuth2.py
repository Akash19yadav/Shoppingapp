from jose import JWTError, jwt
from datetime import datetime, timedelta
from User import schemas
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from User import models
from dependencies import get_db
from sqlalchemy.orm import Session
from config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# This function will create the jwt token with the data and expiration time given by applying the algorithm provided
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# This will verify the token and if it is correct then returns payload present into it otherwise throws exception
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


# This method gets the current user and will be used to secure the endpoints
def get_current_user(request: Request, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="could not authenticate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token_cookie = request.cookies.get('access_token')
    if token_cookie is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="login First")
    scheme, _, token = token_cookie.partition(" ")  # scheme = "Bearer", _ = " ", token = token info without Bearer
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
