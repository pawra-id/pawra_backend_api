from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Text
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
    role = Column(String, nullable=False, server_default='user')
    summary = Column(String, nullable=True)
    address = Column(String, nullable=True)
    image = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

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
    microchip_id = Column(String, nullable=True)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    owner = relationship("User")

activity_tags = Table('activity_tags', Base.metadata,
    Column('activity_id', Integer, ForeignKey('activities.id', ondelete='CASCADE'), nullable=False),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), nullable=False)
)

activity_analysis = Table('activity_analysis', Base.metadata,
    Column('analysis_id', Integer, ForeignKey('analysis.id', ondelete='CASCADE'), nullable=False),
    Column('activity_id', Integer, ForeignKey('activities.id', ondelete='CASCADE'), nullable=False)
)

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    dog_id = Column(Integer, ForeignKey('dogs.id', ondelete='CASCADE'), nullable=False)

    dog = relationship("Dog")
    tags = relationship('Tag', secondary=activity_tags, back_populates='activities')
    analysis = relationship('Analysis', secondary=activity_analysis, back_populates='activities')

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    activities = relationship('Activity', secondary=activity_tags, back_populates='tags')

class Vet(Base):
    __tablename__ = "vets"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    clinic_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    start_work_hour = Column(String, nullable=True)
    end_work_hour = Column(String, nullable=True)
    experience = Column(String, nullable=True)
    education = Column(String, nullable=True)
    image = Column(String, nullable=True)
    description = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    image = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    author = relationship("User")


class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    description = Column(String, nullable=False)
    prediction = Column(String, nullable=False)
    is_shared = Column(Boolean, nullable=False, server_default='FALSE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    dog_id = Column(Integer, ForeignKey('dogs.id', ondelete='CASCADE'), nullable=False)

    dog = relationship("Dog")
    activities = relationship('Activity', secondary=activity_analysis, back_populates='analysis')

