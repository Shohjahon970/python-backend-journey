from fastapi import FastAPI
from database import Base, engine
from  routers.students import router
from models.student import StudentModel
from models.role import RoleModel
from models.user import UserModel

app = FastAPI()
app.include_router(router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message" : "Student Management System"}

@app.get("/about") 
def about():
    return {
        "project": "Student Management System",
        "version": "1.0"
    }


