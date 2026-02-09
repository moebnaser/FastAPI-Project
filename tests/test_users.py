import pytest
from app import schemas
from jose import jwt
from app.config import settings
#all fixtures automatically imported from conftest.py


def test_root(client):
    res = client.get("/")
    assert res.json() == 'Hello, HOME PAGE!!'
    assert res.status_code == 200


def test_user_create(client):
    # trailing slash used because a prefix was used in users.py create
    res = client.post(
        "/users/", json = {"email":"moe.b.naser@gmail.com", "password":"123123"})

    new_user = schemas.UserOut(**res.json())
    assert res.json().get("email") == "moe.b.naser@gmail.com"
    assert res.status_code == 201

def test_login_user(client,test_user):
    res = client.post('/login',
                      data= {"username":test_user["email"], "password":test_user["password"]}) #username as it OAuth2PasswordRequestForm form
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms = [settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "123123", 403),
    ("moe.b.naser@gmail.com", "wrongpassword", 403),
    ("wrongemail@gmail.com", "wrongpassword", 403),
    (None, "123123", 422),
    ("moe.b.naser@gmail.com", None, 422)
])
def test_failed_login(client,test_user, email, password, status_code):
    res = client.post("/login", data = {"username":email, "password":password})
    assert res.status_code == status_code
    #assert res.json().get('detail') == "Invalid Credentials"