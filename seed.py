from models.role import RoleModel
from models.user import UserModel
from database import SessionLocal
from sqlalchemy import select


db = SessionLocal()

def add_role(role_name, db):
    role = db.execute(select(RoleModel).where(RoleModel.name==role_name))
    role = role.scalar_one_or_none()
    if role is None:
        new_role = RoleModel(
            name = role_name
        )
        db.add(new_role)
try:
    add_role("admin",db)
    add_role("student",db)
    db.commit()
finally:
    db.close()

