from fastapi import APIRouter,Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 
#Import db session
from sqlalchemy.orm import Session
from .. import database,schemas,models,utils,auth2
#from ..database import get_db
#from ..schemas import UserLogin

#define our router
router=APIRouter(tags=['authentication'])

@router.post("/login")
#see the changes in the function body
def login(user_credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    #returns
    #username
    #password
    #note usercredential contains username and password
    #query
    user=db.query(models.User).filter(models.User.email==user_credential.username).first()
    #validate
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'invalid credentials')
    
    #verify the password
    #if wrong raise an httpexceptio
    if not utils.verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid credentials')
     
    #create a token and encode what you what eg data=user_id
    access_token=auth2.create_access_token(data ={"user_id":user.id})
    #return token
    return {"access_token":access_token,"token_type":"bear token"}
