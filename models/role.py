from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped, mapped_column,relationship
from database import Base

class RoleModel(Base):
    __tablename__="roles"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False,unique=True)
    users: Mapped[list["UserModel"]] = relationship(back_populates="role")
