from pydantic import BaseModel,ConfigDict

class StudentCreate(BaseModel):
    name: str
    age: int
    major: str

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    major:str
    model_config = ConfigDict(from_attributes=True)


class StudentOperationResponse(BaseModel):
    message:str
    student: StudentResponse

class StudentUpdate(BaseModel):
    name:str | None = None
    age: int | None = None
    major: str| None = None

class UserCreate(BaseModel):
    name: str
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    message: str
