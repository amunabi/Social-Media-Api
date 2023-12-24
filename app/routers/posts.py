from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from typing import List,Optional
from .. import models,schemas,auth2
#import sessions
from sqlalchemy.orm import session
#import engine from db.py
from ..database import get_db
#provides functions like counts and more ,related sql
from sqlalchemy import func

#DEFINE OUR ROUTER
router=APIRouter(
    prefix='/posts',
    tags=['post']
)
#add limit,give a limited search result depending on users interest
#allow users to skip a variety of posts
#@router.get("/",response_model=list[schemas.Post])
@router.get("/",response_model=list[schemas.PostOut])
def get_data(db:session=Depends(get_db),limit:int=10,skip:int=0,search:Optional[str]=""):
    #see search
    #post=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #show post votes number(likes)
    #isouter represents leff outer join
    # .labels the count 
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(results)
    return post

#retrieve a post
@router.get("/{id}",response_model=schemas.PostOut)
def catch_post(id:int,db:session=Depends(get_db)):
    #one_post=db.query(models.Post).filter(models.Post.id==id).first()
    #this solves
    one_post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(
            models.Post.id==id).first()
    #validate
    if not one_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'the {id} cant be found')
    return one_post
#creating a post
#change user_id to current user
@router.post("/",response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db:session=Depends(get_db),current_user:str =Depends(auth2.get_current_user)):
    print(current_user)
    #post_new=models.Post(owner=current_user.id,),
    post_new=models.Post(owner_id=str(current_user.id),**post.model_dump())
    db.add(post_new)
    db.commit()
    db.refresh(post_new)
    return post_new


@router.delete('/{id}')
def delete_post(id:int,db:session=Depends(get_db),current_user:str =Depends(auth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    #validate
    if post==None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'the {id} cant be found')
    
    #authenticate logged in user with owners id ,which are the same
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform the request action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#keeep out for awhile
#@router.put('/{id}')
#def update_post(id:int,updated_post=schemas.PostCreate,db:session=Depends(get_db)):
#    post_query=db.query(models.Post).filter(models.Post.id==id )
#    post=post_query.first()
#
#    if post ==None:
#        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'the {id} doesnt exit')
#    post_query.update(updated_post.model_dump(),synchronize_session=False)
#authenticate logged in user with owners id ,which are the same
#   if post.owner_id != auth2.get_current_user.id:
#        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,details=f"Not authorized to perform the request action")
#
#   db.commit()
#    return post_query.first()