import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine,text


load_dotenv()
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("PG_USER"),
    password= os.getenv("PG_PASSWORD"),
    host = os.getenv("PG_HOST"),
    port = int(os.getenv("PG_PORT","5432")),
    database=os.getenv("PG_DATABASE"),
)
engine = create_engine(DATABASE_URL)


def get_students() :
    with engine.connect() as connection :
        result = connection.execute(
            text("SELECT * FROM students")
        )

        return [
            dict(row._mapping)
            for row in result
        ]

def create_student(student):
    with engine.begin() as connection:
        result = connection.execute(
            text("""
                INSERT INTO students (name, age, major)
                VALUES (:name, :age, :major)
                RETURNING id, name, age, major
"""),
            {
                "name": student.name,
                "age": student.age,
                "major" : student.major
            }
        )   
        return dict(result.fetchone()._mapping)
        
def get_student_by_id(student_id:int):
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT id, name, age, major
                FROM students
                WHERE   id = :student_id
"""),
            {"student_id": student_id}
        )
        row = result.fetchone()

        if row is None:
            return None
        return dict(row._mapping)