from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel
import models
from database import Base, engine,get_db
from sqlalchemy.orm import Session
from sqlalchemy import select



class Student(BaseModel):
    name: str
    age: int
    major: str

app = FastAPI()

Base.metadata.create_all(bind=engine)

students = []
next_student_id = 1

@app.get("/")
def home():
    return {"message" : "Student Management System"}

@app.get("/about") 
def about():
    return {
        "project": "Student Management System",
        "version": "1.0"
    }

@app.get("/students/search")
def get_students_by_major(major: str | None = None, db:Session = Depends(get_db)):
    if major is None:
        result= db.execute(select(models.StudentModel))
        result = result.scalars().all()
        return result
    result = db.execute(select(models.StudentModel).where(models.StudentModel.major.ilike(f"%{major}%")))
    result = result.scalars().all()
    if len(result) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No student found in  {major} major"
        )
    return result
    
 


@app.get("/students/{student_id}")
def get_student_by_id(student_id: int, db : Session=Depends(get_db)):
    result = db.execute(select(models.StudentModel).where(models.StudentModel.id == student_id))
    result = result.scalar_one_or_none()
    if result is not None:
        return result
    raise  HTTPException(
        status_code=404,
        detail=f"No student found with ID {student_id}"
    )
        


@app.post("/students", status_code=201)
def create_student(student: Student, db:Session = Depends(get_db)):
    db_student = models.StudentModel(
        name=student.name,
        age=student.age,
        major=student.major
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return {
        "message":"Student created successfully",
        "student":{
            "id": db_student.id,
            "name": db_student.name,
            "age": db_student.age,
            "major": db_student.major

        }
    }


@app.get("/students")
def get_all_students(db:Session = Depends(get_db)):
    result = db.execute(select(models.StudentModel))
    result = result.scalars().all()
    return result

@app.put("/students/{student_id}")
def update_student(student_id: int, student:Student, db:Session=Depends(get_db)):
    result = db.execute(select(models.StudentModel).where(models.StudentModel.id == student_id))
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
  


@app.delete("/students/{student_id}")
def delete_student(student_id:int, db:Session = Depends(get_db)):
    student = db.execute(select(models.StudentModel).where(models.StudentModel.id == student_id))
    student = student.scalar_one_or_none()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"No student found with ID {student_id}"
        )
    db.delete(student)
    db.commit()
    
