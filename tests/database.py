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
 