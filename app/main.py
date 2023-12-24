from fastapi import FastAPI
#import middleware from course
from fastapi.middleware.cors  import CORSMiddleware
from fastapi import *
from .config import settings
from . import models
from .database import engine
#below code isnt needed,since we have alembic installed already
#note it doest break anything
#models.Base.metadata.create_all(bind=engine)

#make use of router - to make the api run
from .routers import posts,users,auth,vote
app=FastAPI()
#allow api to talk to any browser
#provides all dormain which our api will talk to
#origins= ["https://www.google.com/",
#          "https://www.youtube.com/"]
#make your api public
#use --> 
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],#allows specifc request such as get
    allow_headers=['*'],#allows specific header
)
#upon call the api will check if the search match the following
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)






