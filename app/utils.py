from passlib.context import CryptContext
import bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash (password : str):
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed

def verify (plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)