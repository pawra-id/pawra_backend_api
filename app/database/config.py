from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings as s

SQL_ALCHEMY_DATABASE_URI = f'postgresql://{s.database_username}:{s.database_password}@{s.database_hostname}:{s.database_port}/{s.database_name}'

engine = create_engine(SQL_ALCHEMY_DATABASE_URI)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()