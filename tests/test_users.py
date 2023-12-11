from app.schemes.user import ResponseUser
from app.schemes.token import Token
from jose import jwt
import pytest
from app.config import settings as s

def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "john",
            "email": "johndedu@gmail.com",
            "password": "password",
        },
    )
    new_user = ResponseUser(**response.json())
    assert new_user.email == "johndedu@gmail.com"
    assert response.status_code == 201

def test_login_user(test_user, client):
    response = client.post(
        "/token",
        data={
            "username": test_user['username'],
            "password": test_user['password'],
        }
    )
    login_res = Token(**response.json())
    payload = jwt.decode(login_res.access_token, s.secret_key, algorithms=[s.algorithm])
    id: str = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("username, password, status_code", [
    ('budi', 'password', 403),
    ('john', 'wrong_password', 403),
    (None, 'password', 422),
    ('john', None, 422),
])
def test_login_user_wrong_password(test_user, client, username, password, status_code):
    response = client.post(
        "/token",
        data={
            "username": username,
            "password": password,
        }
    )
    assert response.status_code == status_code

    