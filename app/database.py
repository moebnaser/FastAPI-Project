from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password> @<id_address>/<database name>'
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:123123aA1!@localhost/postgres'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine (SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker (bind= engine,
                             autoflush = False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# 
#PostGres database connection
#======================================
'''
#while True:
try:
    conn = psycopg2.connect(host = "localhost", 
                                database = "postgres",  #this is the database name created in PG addmin
                                user = "postgres", 
                                password = "123123aA1!",
                                cursor_factory = RealDictCursor)
        
    cursor = conn.cursor()
    print ("Database connection successfull")
        
except Exception as error:
    print ("Connecting to database failed")
    print ("Error:", error) 
    time.sleep(2)
#===========================================
'''