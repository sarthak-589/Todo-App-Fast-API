# import sys
# sys.path.append("..")

from typing import Optional
from fastapi import Depends, APIRouter, HTTPException, status, Path
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from routers.auth import get_current_user



router = APIRouter(
    prefix="/address",
    tags=["address"],
    responses={404: {"description": "Not Found"}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Address(BaseModel):
    address: str
    city: str
    state: str
    country: str    
    pin_code: str
    apt_num: Optional[int]


@router.post("/")
async def create_address(address: Address, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    address_model = models.Address()
    address_model.address = address.address
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.pin_code = address.pin_code
    address_model.apt_num = address.apt_num

    db.add(address_model)
    db.flush()    

    '''This is a SQLAlchemy method that sends the pending changes to the database. It ensures that the address_model gets a primary key value assigned before proceeding. Unlike commit(), flush() does not finalize the transaction but synchronizes the session with the database.'''

    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    user_model.address_id = address_model.id

    db.add(user_model)

    db.commit()


@router.get("/all")
async def get_all_address(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    if user_model is None or user_model.address_id is None:
        raise HTTPException(status_code=404, detail='No address found.')
    
    '''models.Users.id == user.get("id") specifies the condition: it compares the id column of the Users table with the id value from the user dictionary.'''

    '''user.get("id") retrieves the id value from the user dictionary. get method is used to safely retrieve the value, returning None if the key does not exist.'''

    '''.first() executes the query and returns the first result. If no matching record is found, it returns None.'''
    
    address_model = db.query(models.Address).filter(models.Address.id == user_model.address_id).first()

    if address_model is None:
        raise HTTPException(status_code=404, detail="Address not found") 
    
    '''models.Address.id == user_model.address_id specifies the condition: it compares the id column of the Address table with the address_id value from the user_model.'''

    '''user_model.address_id retrieves the address_id attribute from the user_model instance, which was queried earlier and represents the logged-in user.'''
    
    return address_model


'''user: dict = Depends(get_current_user):- Uses dependency injection to get the current user as a dictionary. The get_current_user function is expected to return user information if the user is authenticated.'''


'''db: Session = Depends(get_db):- Uses dependency injection to get a database session from the get_db function, which manages the database connection.'''


@router.put("/update")
async def update_address(address: Address, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    if user_model is None or user_model.address_id is None:
        raise HTTPException(status_code=404, detail="Address Not Found")
    
    address_model = db.query(models.Address).filter(models.Address.id == user_model.address_id).first()

    if address_model is None:
        raise HTTPException(status_code=404, detail="Address not found")
    
    address_model.address = address.address
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.pin_code = address.pin_code
    address_model.apt_num = address.apt_num

    db.add(address_model)
    db.commit()
    return {"message": "Address Updated Successfully"}


@router.delete("address/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(user: dict = Depends(get_current_user), address_id: int = Path(gt=0), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    if user_model is None or user_model.address_id != address_id:
        raise HTTPException(status_code=404, detail="Address Not Found")
    
    address_model = db.query(models.Address).filter(models.Address.id == address_id).first()
    
    if address_model is None:
        raise HTTPException(status_code=404, detail="Address Not Found")
    
    db.delete(address_model)
    db.commit()

    # Reset user's address_id to None after deletion
    user_model.address_id = None
    db.add(user_model)
    db.commit()

    return {"detail": "Address Deleted Successfully"}