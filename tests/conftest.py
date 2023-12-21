from fastapi.testclient import TestClient
from app.main import app
import pytest
from app import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.oauth2 import create_token
from app.config import settings as s
from fastapi_pagination import add_pagination
from app.database.config import get_db, Base

SQL_ALCHEMY_DATABASE_URI = f'postgresql://{s.database_username}:{s.database_password}@{s.database_hostname}:{s.database_port}/{s.database_name}_test'
engine = create_engine(SQL_ALCHEMY_DATABASE_URI)
testSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def get_db_override():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = get_db_override
    add_pagination(app)
    yield TestClient(app)

@pytest.fixture()
def test_user(client):
    user_data = {"email": "johndedu@gmail.com", "username": "john", "password": "password"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201

    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture()
def test_user_admin(client):
    user_data = {"email": "admin@gmail.com", "username": "admin", "password": "password", "role": "admin"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201

    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture()
def token(test_user):
    return create_token(data={"user_id": test_user['id']})

@pytest.fixture()
def token_admin(test_user_admin):
    return create_token(data={"user_id": test_user_admin['id']})

@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
        }
    return client

@pytest.fixture()
def authorized_client_admin(client, token_admin):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_admin}"
        }
    return client

@pytest.fixture()
def test_blog(test_user_admin, session):
    blog_data = [
        {"title": "test blog", "content": "test content"},
        {"title": "test blog 2", "content": "test content 2"},
        {"title": "test blog 3", "content": "test content 3"},
    ]
    #insert blogs to db
    for blog in blog_data:
        blog['author_id'] = test_user_admin['id']
        session.add(models.Blog(**blog))
    session.commit()
    return session.query(models.Blog).all()
  
