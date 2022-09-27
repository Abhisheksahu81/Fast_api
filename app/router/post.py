from itertools import groupby
from .. import models
from ..database import engine , get_db
from ..schemas import PostBase, CreatePost
from .. import schemas, oauth2
from fastapi import FastAPI , Response , HTTPException , status, Depends, APIRouter, Depends
from urllib import response
from sqlalchemy.orm import session
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/" ,response_model = list[schemas.PostOut])
def get_posts(db:session = Depends(get_db), user_id : int =  Depends(oauth2.get_current_user)):
  
    posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id == models.Post.id , isouter = True).group_by(models.Post.id).all()
    return posts
    
 

@router.post("/" , status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def create_post(post:CreatePost, db:session = Depends(get_db) ,user_id : int =  Depends(oauth2.get_current_user)):
    print(user_id)
  
    new_post = models.Post(owner_id = user_id.id ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # we have to convert sqlalchemy model to pydantic model for response
    return new_post

@router.get("/{id}" , response_model = schemas.PostOut)
def get_one_post(id:int , response : Response, db:session=Depends(get_db)):
    # cursor.execute(f"""SELECT * FROM posts where id = (%s)""" , (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id ==models.Post.id , isouter = True).group_by(models.Post.id).filter(id==models.Post.id).first()
    if not post:
    #   response.status_code = 404
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail="POst not found")
    return post   

@router.delete('/{id}')
def delete_post(id : int , status_code = status.HTTP_204_NO_CONTENT , 
        db:session = Depends(get_db)  , user_id : int =  Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()   
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"POst not found")

    if post.owner_id != int(user_id.id): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = "Not authorized to perform requested action")
    post_query.delete(synchronize_session = False)
    db.commit()    
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update(id: int , updated_post : CreatePost ,
             db:session = Depends(get_db),user_id : int =  Depends(oauth2.get_current_user)):  
  

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post  =post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f"Post not found")
    
    if post.owner_id != int(user_id.id): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = "Not authorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    db.refresh(post)
    return {'updated post' : post}

