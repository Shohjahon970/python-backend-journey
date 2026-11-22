from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from sqlalchemy import Integer, String,Boolean,ForeignKey
from models.role import RoleModel



class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"),nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[RoleModel] = relationship(back_populates="users")
    student: Mapped["StudentModel"] = relationship(back_populates="user")