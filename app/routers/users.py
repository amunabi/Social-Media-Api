from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,utils,schemas
#import sessions
from sqlalchemy.orm import session
#import engine from db.py
from ..database import get_db

#DEFINE OUR ROUTER
router=APIRouter(
    prefix="/users",
    tags=['user']
)

#User Registration
#create a new user account
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:session=Depends(get_db)):
    #create the hash of the password - user.password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#retrieve specific user based on their id
@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.UserOut) 
def get_users(id:int,db:session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()

    #validate
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"the entry {id} doesnt exit")
    
    return user