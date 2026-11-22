from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select,or_
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate,UserResponse,UserLogin
from models.role import RoleModel
from models.student import StudentModel
from security import hash_password,verify_password
from models.user import UserModel
from sqlalchemy.exc import IntegrityError
from security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

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
        db.flush()
        new_student = StudentModel()
        new_student.age= user.age
        new_student.major = user.major
        new_student.name = user.name
        new_student.user = new_user
        db.add(new_student)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Registration conflicts with existing data"
        )
    return {
        "message":"Registration successful"
    }


@router.post("/login")
def login_user(user: UserLogin, db:Session = Depends(get_db)):
    check_identifier = db.execute(select(UserModel).where(or_(UserModel.email == user.identifier, UserModel.username == user.identifier)))
    check_identifier = check_identifier.scalar_one_or_none()
    if check_identifier is None:
        raise HTTPException (
            status_code=401,
            detail= "Invalid credentials"
        )
    password_check = verify_password(user.password, check_identifier.password_hash)
    if not password_check:
        raise HTTPException (
            status_code=401,
            detail = "Invalid credentials"
        )
    if not check_identifier.is_active:
        raise HTTPException (
            status_code=403,
            detail="Your account is inactive"
        )
    access_token = create_access_token(check_identifier.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/token")
def get_token(db: Session = Depends(get_db), form_data : OAuth2PasswordRequestForm = Depends()):
    current_user = db.execute(select(UserModel).where(or_(form_data.username == UserModel.username, form_data.username == UserModel.email)))
    current_user = current_user.scalar_one_or_none()
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    password_check = verify_password(form_data.password, current_user.password_hash)
    if not password_check:
        raise HTTPException (
            status_code=401,
            detail="Incorrect username or password"
        )
    if current_user.is_active is False:
        raise HTTPException(
            status_code=403,
            detail="Your account is inactive"
        )
    access_token = create_access_token(current_user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }