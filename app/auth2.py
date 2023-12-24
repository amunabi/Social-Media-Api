#implementing the jwt tokens
from jose import JWTError,jwt
from datetime import datetime,timedelta
from  . import schemas,models,database
from fastapi import status,HTTPException,Depends
from sqlalchemy.orm import Session
#access the databse
#import passport bearer
from fastapi.security import OAuth2PasswordBearer
#specific tokenurl ,our end point connection
#copy the "/login" from auth.py file
auth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
#provide
#secret_key
#algorithm
#expiration time for a user loged in
#import .config file
from  .config import settings
SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES= settings.access_token_expire_min
#settings.access_token_expire_min


def create_access_token(data: dict):
    to_encode=data.copy()
    #grab the current time and add 30 minute,a time for expiration
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    #create jwt token
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt


#create a fnction to verify the access token
#decode the code
def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=str(id)) 
    except JWTError:
        raise credentials_exception
    return token_data

#below will  verify the user by callin g the verify_access_token
#wil get the current user id
#pass the auth2_scheme (represents password bearer)
def get_current_user(token:str= Depends(auth2_scheme),db:Session=Depends(database.get_db)):
    #create our exception
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                       detail=f"could not validate credentials",
                                       headers={"WWW-Authenticate":"Bearer"})
    #create token
    #access the verify function
    token=verify_access_token(token,credential_exception)
    #query the database
    user=db.query(models.User).filter(models.User.id==token.id).first()
    #return verify_access_token
    return user