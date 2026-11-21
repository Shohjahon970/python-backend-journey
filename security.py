from pwdlib import PasswordHash 
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models.user import UserModel
from fastapi import Depends, HTTPException
import jwt
from config import JWT_SECRET_KEY
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")
pasword_hasher = PasswordHash.recommended()
def hash_password(password):
    result = pasword_hasher.hash(password)
    return result
def verify_password(password,hashed_password):
    return pasword_hasher.verify(password,hashed_password)


def create_access_token(user_id: int):
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload = {
        "sub": str(user_id),
        "exp": expire_time
    }
    access_token=jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return access_token

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )
    try:
        user_id = int(payload["sub"])
    except (KeyError, ValueError):
        raise HTTPException (
            status_code= 401,
            detail="Invalid token"
        )
    current_user = db.execute(select(UserModel).where(UserModel.id == user_id))
    current_user =current_user.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    return current_user

def require_admin(current_user: UserModel = Depends(get_current_user)):
    if current_user.role.name !="admin":
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to perform this action"
        )
    return current_user