from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.config import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    breed = Column(String, nullable=False)
    neutered = Column(Boolean, nullable=True, server_default='FALSE')
    color = Column(String, nullable=True)
    weight = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    owner = relationship("User")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    dog_id = Column(Integer, ForeignKey('dogs.id', ondelete='CASCADE'), nullable=False)

    dog = relationship("Dog")