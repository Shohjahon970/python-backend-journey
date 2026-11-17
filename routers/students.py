from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import select
from models.student import StudentModel
from schemas import StudentCreate,StudentResponse,StudentOperationResponse,StudentUpdate
from fastapi import APIRouter,Depends,HTTPException

router = APIRouter(
    prefix="/students",
    tags=["students"]
)

@router.get("/",response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    result = db.execute(select(StudentModel))
    result = result.scalars().all()
    return result

@router.post("/", status_code=201, response_model=StudentOperationResponse)
def create_student(student:StudentCreate, db:Session = Depends(get_db)):
    db_student = StudentModel(
        name = student.name,
        age = student.age,
        major = student.major
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return {
        "message" : "Student created Successfully.",
        "student": {
            "id": db_student.id,
            "name": db_student.name,
            "age": db_student.age,
            "major": db_student.major

        }
    }
@router.get("/search")
def get_students_by_major(major: str | None = None, db:Session = Depends(get_db)):
    if major is None:
        result= db.execute(select(StudentModel))
        result = result.scalars().all()
        return result
    result = db.execute(select(StudentModel).where(StudentModel.major.ilike(f"%{major}%")))
    result = result.scalars().all()
    if len(result) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No student found in  {major} major"
        )
    return result


@router.get("/{student_id}",response_model = StudentResponse)
def get_student_by_id(student_id: int, db : Session=Depends(get_db)):
    result = db.execute(select(StudentModel).where(StudentModel.id == student_id))
    result = result.scalar_one_or_none()
    if result is not None:
        return result
    raise  HTTPException(
        status_code=404,
        detail=f"No student found with ID {student_id}"
    )

@router.put("/{student_id}",response_model=StudentOperationResponse)
def update_student(student_id: int, student:StudentCreate, db:Session=Depends(get_db)):
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
def update_student_info(student_id:int,student:StudentUpdate, db:Session = Depends(get_db)):
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
def delete_student(student_id:int, db:Session = Depends(get_db)):
    student = db.execute(select(StudentModel).where(StudentModel.id == student_id))
    student = student.scalar_one_or_none()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"No student found with ID {student_id}"
        )
    db.delete(student)
    db.commit()



