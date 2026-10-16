from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from database import get_students, create_student, get_student_by_id

class Student(BaseModel) :
    name: str = Field(min_length= 2)
    age: int = Field(ge = 0)
    major: str

app = FastAPI()
students = []
next_student_id = 1


@app.get("/")
def home():
    return {"message": "My Python backend journey starts here!"}


@app.get("/about")
def about():
    return {
        "major": "Software Engineering",
        "goal": "Become a Backend Developer"
    }

@app.get("/greet")
def greet(name:str = "bro") :
    return {
        "message" : f'Hello, {name}'
    }
@app.get("/students/{student_id}")
def read_student(student_id : int) :
    student = get_student_by_id(student_id)

    if student is None :
        raise HTTPException(
            status_code = 404,
            detail = "Student not found"
        )
    return student
 

@app.post("/students", status_code=201)
def add_student(student: Student) :
    return create_student(student)
 

@app.get("/students")
def read_students() :
    return get_students()



