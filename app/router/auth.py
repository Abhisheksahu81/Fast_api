

from fastapi import FastAPI, APIRouter, Depends , HTTPException , status
from sqlalchemy.orm import Session
from app.schemas import UserLogin
from ..database import get_db
from ..utility import verify
from app import models, oauth2,schemas


router = APIRouter(
    tags= ["Login"]
)

@router.post("/login" , response_model=schemas.Token)
def login(user_credentials : UserLogin , db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= "Invalid Credentials")

    if not verify(user_credentials.password , user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= "Invalid Credentials")
  
    #create token
    token = oauth2.create_jwt_token(data = {"user_id" : user.id})
    return{"access_token" : token  , "token_type" : "bearer"}

