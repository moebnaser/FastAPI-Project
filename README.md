
# Backend service using FastAPI (Python) for a social media app prototype 

## KEY TERMS: (FastAPI, JWT, outh2, SqlAlchemy, Alembic migration, PostgresSql, Server side application, Backend, WebAPI)

## Project Contents:

### - FastAPI with 4 routes
 1) Posts route: This route is reponsible for creating post, deleting post, updating post and Checking posts
 2) Users route: This route is about creating users and searching user by id
 3) Auth route: This route is about login system and authentication
 4) Vote route: This route is about likes or vote system and this route contain code for upvote or remove vote, there is not logic about down vote

### - Authentication logic (JWT Token decoding/encoding, outh2 authentication and authorization logic for POST/GET/DELETE/UPDATE path operations)
### - PostgresSql database with SqlAlchemy models and Alembic versioning and migration
### - Pydantic models validation for request and response
### - Test fixtures to validate logic for each route (users, posts, vote, auth) - pytest
### - Docker file and Docker-compose (image and containerization) with database service
### - CI/CD pipeline/workflow (build, test) and (deploy on Heroku server and Ubuntu servers). (YML)

### how to run locally
First clone this repo by using following command
````
git clone https://github.com/moebnaser/FastAPI-Project
````
then 
````
cd FastAPI-Project
````
Then install fastapp using all flag like 
```
pip install fastapi[all]
````
Then go this repo folder in your local computer run follwoing command
````
uvicorn main:app --reload
````
Then you can use following link to use the  API
````
http://127.0.0.1:8000/docs 
````

### After run this API you need a database in postgres 
Create a database in postgres then create a file name .env and write the following things in you file 
````
DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = passward_that_you_set
DATABASE_NAME = name_of_database
DATABASE_USERNAME = User_name
SECRET_KEY = 09d25e094faa2556c818166b7a99f6f0f4c3b88e8d3e7 
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60(base)
````
### Note: SECRET_KEY in this exmple is just a psudo key. You need to get a key for youself and you can get the SECRET_KEY  from fastapi documantion

 
