
from .. import models,schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. database import  get_db
from sqlalchemy.orm import Session
from typing import  List, Optional
from .. import oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts"
)

@router.get("/", response_model= List[schemas.PostOut] )
def get_posts(db:Session = Depends(get_db),user_id:int = Depends(oauth2.get_current_user),
              limit:int = 10, skip:int=0, search:Optional[str]=""):

    posts = db.query(models.Post).filter(models.Post.owner_id == user_id.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True
    ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results



@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post : schemas.PostCreate, db:Session = Depends(get_db), 
                user_id:int = Depends(oauth2.get_current_user)):
    print(type(user_id))
    new_post = models.Post(owner_id = user_id.id, **post.dict())
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post 




@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), user_id:int = Depends(oauth2.get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id==id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True
    ).group_by(models.Post.id).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id {id} is not found")
    if post[0].owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    return post




@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),user_id:int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session = False)
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)


#updating the post 
@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, update_post : schemas.PostCreate, db: Session = Depends(get_db),
                user_id:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=404,detail=f"Post with id {id} not found")
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    # post_query.update({'title':'Ths is hard coded title','content':'This is hard coded content'}, synchronize_session = False)
    post_query.update(update_post.dict(), synchronize_session = False)
    db.commit()
    return post_query.first()


