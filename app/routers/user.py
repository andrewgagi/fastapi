from fastapi import  Depends, HTTPException, Response, status,APIRouter

from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,utils,schemas
router=APIRouter(prefix="/users",tags=['users'])
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    # hash the passowrd
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}",response_model=schemas.User)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id:{id} not found")
@router.get("/",response_model=list[schemas.User])
def get_users(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    return users

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_users(id:int ,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id:{id} not found")
    user.delete(synchronize_session=False)
    db.commit()
    Response("user deleted successfully")
@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED,response_model=schemas.User)
def update_user(id:int,user:schemas.UserBase,db:Session=Depends(get_db)):
    update_query=db.query(models.User).filter(models.User.id==id)
    if not update_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id:{id} not found")
    update_query.update(user.dict(),synchronize_session=False)
    db.commit()
    return update_query.first()
