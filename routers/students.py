from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import and_, select
from models.student import StudentModel
from models.user import UserModel
from schemas import StudentCreate,StudentResponse,StudentOperationResponse,StudentUpdate
from fastapi import APIRouter,Depends,HTTPException
from security import get_current_user, require_admin

router = APIRouter(
    prefix="/students",
    tags=["students"]
)

@router.get("/",response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    if current_user.role.name =="admin":
        result = db.execute(select(StudentModel))
        result = result.scalars().all()
        return result
    elif current_user.role.name == "student":
        if current_user.student is None:
            raise HTTPException(
                status_code=404,
                detail="Not Found"
            )
        return [current_user.student]



@router.get("/search",response_model =list[StudentResponse])
def get_students_by_major(major: str | None = None, db:Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    if current_user.role.name =="student":
        if current_user.student is None:
            raise HTTPException(
                status_code=404,
                detail="Not Found"
            )
        if major is None:
            return [current_user.student]
        result = db.execute(select(StudentModel).where(and_(StudentModel.major.ilike(f"%{major}%"), StudentModel.id == current_user.student.id)))
        result = result.scalar_one_or_none()
        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Not Found"
            )
        return [result]
    if major is None:
        result= db.execute(select(StudentModel))
        result = result.scalars().all()
        return result
    
    result = db.execute(select(StudentModel).where(StudentModel.major.ilike(f"%{major}%")))
    result = result.scalars().all()
    if len(result) == 0:
        raise HTTPException(
            status_code=404,
            detail=
            f"No student found in  {major} major"
        )
    return result


@router.get("/{student_id}",response_model = StudentResponse)
def get_student_by_id(student_id: int, db : Session=Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    result = db.execute(select(StudentModel).where(StudentModel.id == student_id))
    result = result.scalar_one_or_none()
    if result is not None:
        if current_user.role.name =="student":

            if current_user.student is not None and current_user.student.id == student_id:
                return result
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Not Found"
                )
        return result
    raise  HTTPException(
        status_code=404,
        detail="Not Found"
    )

@router.put("/{student_id}",response_model=StudentOperationResponse)
def update_student(student_id: int, student:StudentCreate, db:Session=Depends(get_db), admin: UserModel = Depends(require_admin)):
    result = db.execute(select(StudentModel).where(StudentModel.id == student_id))
    result = result.scalar_one_or_none()
    if result is None:
        raise HTTPException (
            status_code=404,
            detail=f"No student found with ID {student_id}"
        )
    result.name = student.name
    result.age = student.age
    result.major = student.major
    db.commit()
    db.refresh(result)
    return {
        "message":"Student updated successfully.",
        "student":result
    }

@router.patch("/{student_id}",response_model=StudentOperationResponse)
def update_student_info(student_id:int,student:StudentUpdate, db:Session = Depends(get_db), admin:UserModel = Depends(require_admin)):
    db_student = db.execute(select(StudentModel).where(StudentModel.id == student_id))
    db_student= db_student.scalar_one_or_none()
    if db_student is None:
        raise HTTPException(
            status_code=404,
            detail=f"No student found with ID {student_id}"
        )
    update_data = student.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )
    for field, value in update_data.items():
        setattr(db_student,field, value)
    db.commit()
    db.refresh(db_student)
    return {
        "message":"Student updated successfully.",
        "student":db_student
    }


@router.delete("/{student_id}")
def delete_student(student_id:int, db:Session = Depends(get_db), admin: UserModel = Depends(require_admin)):
    student = db.execute(select(StudentModel).where(StudentModel.id == student_id))
    student = student.scalar_one_or_none()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"No student found with ID {student_id}"
        )
    db.delete(student)
    db.commit()


