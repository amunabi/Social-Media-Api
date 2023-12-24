#hold bunch of utlities function
#import passlib function for hashing a password
from passlib.context import CryptContext

#define the cryptcontext
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


#define a functio that we can call
def hash(password:str): 
    return pwd_context.hash(password)


#responsible to compare the 2 hshing of front end password and db hashed password
#verify password
def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)