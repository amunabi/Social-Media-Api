#this manages all our environment variable configurations.
#handles password ,secrets keys
#all values will be a string,bt the initial input will be translated as an integer
from pydantic_settings import BaseSettings
#set our environment for our database connection
class Setting(BaseSettings):
    database_hostname:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str #siging our token
    access_token_expire_min:int
   
    #TELL OUR FILE TO IMPORT VARIABLE VALUES FROM .ENV FILE
    class Config:
        env_file='.env'

settings=Setting()