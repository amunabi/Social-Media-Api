from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
#schema for handling login
class UserLogin(BaseModel):
    #column for login
    email:EmailStr
    password:str

#handle user registration
class UserCreate(BaseModel):
    email:EmailStr
    password:str

#redefine the response
class UserOut(BaseModel):
    id:int
    email:EmailStr
    create_at:datetime
    class config:
        orm_mode=True

       

class PostBase(BaseModel):
    title :str
    content :str
    published :bool=True

#inheritance

class PostCreate(PostBase):
    pass 
    #accepts whatever is con tained in postbase model    

#define  a response
class Post(PostBase):
    #restrict columns for the users to view
    id:int
    create_at:datetime
    #add owner_id
    owner_id:int
    #recall userout  class name ,this will generate our user's info automatically
    owner:UserOut
    class config:
        orm_mode=True

#handle the joins in get/post
class PostOut(BaseModel):
    Post:Post
    votes:int
    class config:
        orm_mode=True


#scheman for token
class Token(BaseModel):
    access_token:str
    token_type:str  


class TokenData(BaseModel):
    id: Optional[str]=None       



#handles votes
class Vote(BaseModel):
    post_id:int
    #import connint to validate if var below has 0 or 1
    #le=1 means less 1 = 1
    dir:conint(le=1)


