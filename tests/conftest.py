import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.database import Base, engine
from app import models
from sqlalchemy.ext.declarative import declarative_base
from alembic import command
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:123123aA1!@localhost:5432/fastapi_test'

engine = create_engine (SQLALCHEMY_DATABASE_URL)

Base.metadata.create_all(bind = engine)

TestingSessionLocal = sessionmaker (bind= engine,
                             autoflush = False)

@pytest.fixture() #scope = "module" to run once per module not once per test
def session():
    #command.upgrade("head")
    #command.downgrade("base")
    #run code before runnig our test
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db        
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email":"moe.b.naser@gmail.com", 
                 "password": "123123"}
    res = client.post("/users/", json= user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email":"123r@gmail.com", 
                 "password": "123123"}
    res = client.post("/users/", json= user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token ({"user_id":test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{"title":"title 1",
                   "content":"content 1",
                   "user_id": test_user['id']
                   },
                   {"title":"title 2",
                   "content":"content 2",
                   "user_id": test_user['id']
                   },
                   {"title":"title 3",
                   "content":"content 3",
                   "user_id": test_user['id']},
                    {"title":"title 3",
                   "content":"content 3",
                   "user_id": test_user2['id']}]
    
    def create_post_model(post):
        return models.Post(**post)
    posts_map = map (create_post_model, posts_data)
    posts = list(posts_map)
    session.add_all(posts)
    session.commit()

    posts = session.query (models.Post).all()
    return posts