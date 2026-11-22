from sqlalchemy import Integer,String,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class StudentModel(Base):
    __tablename__="students"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    major: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    user: Mapped["UserModel"] = relationship(back_populates="student")
