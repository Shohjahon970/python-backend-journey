from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate,UserResponse
from models.role import RoleModel
from security import hash_password
from models.user import UserModel
from sqlalchemy.exc import IntegrityError
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register", response_model=UserResponse,status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    role = db.execute(select(RoleModel).where(RoleModel.name =="student"))
    role = role.scalar_one_or_none()
    if role is None:
        raise HTTPException(
            status_code=404,
            detail="No student role"
        )
    check_username = db.execute(select(UserModel).where(UserModel.username == user.username))
    check_username = check_username.scalar_one_or_none()
    if check_username is not None:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )
    check_email = db.execute(select(UserModel).where(UserModel.email == user.email))
    check_email = check_email.scalar_one_or_none()
    if check_email is not None:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )
    hashed_password = hash_password(user.password)
    new_user = UserModel()
    new_user.name = user.name
    new_user.username = user.username
    new_user.email = user.email
    new_user.role = role
    new_user.password_hash = hashed_password
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Registration conflicts with existing data"
        )

    db.refresh(new_user)
    return {
        "message":"Registration successful"
    }