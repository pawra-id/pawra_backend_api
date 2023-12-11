from app.schemes.blog import ResponseBlog
from app import models

def test_get_all_blogs(authorized_client, test_blog):
    response = authorized_client.get("/blogs/")
    def validate(blog):
        return ResponseBlog(**blog)
    map(validate, response.json()['items'])
    assert response.status_code == 200
    assert len(response.json()['items']) == len(test_blog)

def test_unauthorized_get_all_blogs(client, test_blog):
    response = client.get("/blogs/")
    assert response.status_code == 401

def test_get_blog_by_id(authorized_client, test_blog):
    response = authorized_client.get(f"/blogs/{test_blog[0].id}")
    assert response.status_code == 200
    assert response.json()['title'] == test_blog[0].title

def test_unauthorized_get_blog_by_id(client, test_blog):
    response = client.get(f"/blogs/{test_blog[0].id}")
    assert response.status_code == 401

def test_get_blog_by_id_not_found(authorized_client, test_blog):
    response = authorized_client.get(f"/blogs/999")
    assert response.status_code == 404