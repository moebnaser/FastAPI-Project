from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2


router = APIRouter(prefix = "/posts", tags= ["posts"])

# API HTTP requests Methods 
#=============================
@router.get("/", response_model = List[schemas.PostOut]) # if both paths point to same location, the first match returned
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
               limit: int = 10, skip: int = 0, search : Optional[str] = ""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts  = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
                                    models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts



@router.post("/", status_code= status.HTTP_201_CREATED, response_model = schemas.Post) 
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)): #pydantic class does all data validation and format
    #could do it with string format but that would be a vulnrability to SQL injection, where the user inputs SQL commands
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                   #(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(user_id = current_user.id , **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Reloads the object from the database This is important because:The database may have generated values (like id, created_at) After this, new_post.id will exist 
    return  new_post





@router.get("/{id}",  response_model = schemas.PostOut)
def get_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = (%s) """, (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
                                    models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                             detail=  f"post with {id} was not found")
    else:
        return post




@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} Does NOT Exist")

    if post.user_id != current_user.id:
        raise HTTPException (status_code= status.HTTP_403_FORBIDDEN,
                             detail = "Not Authoerized to performe Delete")
    
    post_query.delete(synchronize_session= False)
    db.commit()



@router.put("/{id}",  response_model = schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #              (post.title, post.content, post.published, (str(id))))
    #updated_post = cursor.fetchone()
    #conn.commit()
    query = db.query(models.Post).filter(models.Post.id == id)
    old_post = query.first()

    if old_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} Does NOT Exist")
    
    if old_post.user_id != current_user.id:
        raise HTTPException (status_code= status.HTTP_403_FORBIDDEN,
                             detail = "Not Authoerized to performe Delete")  
      
    query.update(post.dict(), synchronize_session= False)
    db.commit()
    return  query.first()
#+