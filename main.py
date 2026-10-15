from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException

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
def get_student(student_id : int) :
    for student in students :
        if student["id"] == student_id :
            return student
    raise HTTPException(
        status_code= 404,
        detail="Student not found"
    )

@app.post("/students", status_code=201)
def create_student(student: Student) :
    global next_student_id
    new_student = student.model_dump()
    new_student["id"] = next_student_id
    students.append(new_student)
    next_student_id +=1
    return new_student

@app.get("/students")
def get_students() :
    return students
