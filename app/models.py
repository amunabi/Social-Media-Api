from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
#define model
#handle user registration
class User(Base):
    __tablename__="users"
    #columns
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    create_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    phone_no=Column(String)

class Post(Base):
    #define the table names
    __tablename__ ="posts"

    #define column
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='true',nullable=False)
    create_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    #create a reference column ,refers to user id from users table 
    #with a foreign key constraints
    #foreignkey("users.id") note it is rerefencing the user table on the id column
    owner_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    #returns the class of another model
    #User refers to the class name and not the table name
    owner=relationship("User")




#handles votes model
class Vote(Base):
    __tablename__="votes"
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
