from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from typing import List,Optional
from .. import models,schemas,auth2
#import sessions
from sqlalchemy.orm import session
#import engine from db.py
from ..database import get_db
#DEFINE OUR ROUTER
router=APIRouter(
    prefix='/votes',
    tags=['vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def cast_vote(vote:schemas.Vote,db:session=Depends(get_db),current_user:str=Depends(auth2.get_current_user)):
    #verify if a post exist
    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not  post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post id {vote.post_id} doesnt exist")
    #query to see if the vote exist
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    #set logic if vote ==1
    if (vote.dir==1):
        #if found the post the user already voted the post
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f'@{current_user.id} you have already voted a post with  an id of {vote.post_id}')
        #if  we didnt find a post ,then vote by creating a vote
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        #we arent returning any vote to the user bt a message
        return {"message":"a vote was made successfully"}
    #   
    else:
        #we cant delete a post isnt in the database
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='vote doesnt exist')
        #if a vote was found,then delete
        #0 represents delete
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"a vote was deleted succcessfully"}