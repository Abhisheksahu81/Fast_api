
from ctypes import util
from .. import models
from ..database import engine , get_db
from ..schemas import PostBase, CreatePost
from .. import schemas
from fastapi import FastAPI , Response , HTTPException , status, Depends, APIRouter
from sqlalchemy.orm import session
from ..utility import hash
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/" , status_code=status.HTTP_201_CREATED, response_model = schemas.Userout)
def create_users(user : schemas.UserCreate , db : session = Depends(get_db) , user_id : int = Depends(get_current_user)):
    user.password = hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/" , response_model= list[schemas.Userout])
def getusers(db : session = Depends(get_db), user_id : int = Depends(get_current_user)):
    users = db.query(models.User).all()
    return users    

@router.get("/{id}" , response_model=schemas.Userout)
def getusers(id : int, db : session = Depends(get_db) , user_id : int = Depends(get_current_user)):
    users = db.query(models.User).filter(models.User.id == id).first() 
    if not users :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User Not Found")
    return users        