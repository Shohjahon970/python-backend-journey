from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET_KEY= os.getenv("JWT_SECRET_KEY")

if JWT_SECRET_KEY is None:
    raise ValueError("JWT_SECRET_KEY is missing from environment variables")
