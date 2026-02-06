from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import  get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix = "/users", tags = ["users"])


# user path operations
@router.post("/", status_code= status.HTTP_201_CREATED, response_model = schemas.UserOut) 
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)): #pydantic class does all data validation and format

    #could do it with string format but that would be a vulnrability to SQL injection, where the user inputs SQL commands
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                   #(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()

    password_hash = utils.hash(user.password)

    # If utils.hash returns bytes, decode it to a clean string
    if isinstance(password_hash, bytes):
        password_hash = password_hash.decode('utf-8')

    user.password = password_hash

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Reloads the object from the database This is important because:The database may have generated values (like id, created_at) After this, new_post.id will exist 
    return  new_user


@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id: int, db:Session = Depends(get_db), current_user: int = Depends (oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"User{id} does not exist")

    return user
