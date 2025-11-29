from sqlmodel import SQLModel, create_engine
import os

# Use environment variable or fallback
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:pass@db:3306/mydb"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

