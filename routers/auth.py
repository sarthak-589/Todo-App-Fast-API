from datetime import timedelta, datetime
from typing import Annotated
from typing_extensions import deprecated
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError



router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


SECRET_KEY = 'c3c287ea8285280cd50252196d4b5eeed07805bc02cee7dff2f071d69498316e'
ALGORITHM = 'HS256'




bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


'''CryptContext is a class from the passlib library, which provides a unified way to manage multiple password hashing schemes.'''

'''schemes=['bcrypt'] specifies that the bcrypt hashing algorithm should be used for password hashing.'''

'''deprecated='auto' indicates that deprecated hashing algorithms should be handled automatically, ensuring backward compatibility and security.'''

'''OAuth2PasswordBearer is a class from the fastapi.security module that provides an OAuth2 password flow for API token authentication.'''

'''tokenUrl='auth/token' specifies the endpoint where the client can obtain the JWT token. In this case, it points to the /auth/token URL.'''



class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


'''def get_db():- This line defines a function named get_db. The purpose of this function is to provide a database session for the duration of a request.'''


'''SessionLocal() is called to create a new SQLAlchemy session object. This session object (db) is used to interact with the database. `SessionLocal` is typically a factory function created by SQLAlchemy's sessionmaker which is configured with the database connection parameters.'''

'''try:- This line starts a try block. The try block is used to ensure that the db session is properly closed after its use, even if an error occurs.'''

'''yield db:- is used here because this function is a generator. In FastAPI, generator functions can be used to manage resources that need to be set up and cleaned up around the processing of a request.
It pauses the function and returns the db session object to the caller (typically a dependency injection in a route handler).'''


'''Finally:- The finally block contains code that runs no matter what—whether an exception is raised or not. It ensures that the cleanup code (closing the session) runs.'''


'''db.close:- This line closes the database session. Closing the session is important to release the connection back to the connection pool and to prevent resource leaks.'''


'''db_dependency:- This line defines a variable named db_dependency. This variable will hold an annotated dependency.'''


'''Annotated:- is used to provide additional context and metadata to type hints. Adds clarity and context to the type hints, making it clear that the type is associated with a specific dependency.'''


'''Session:- Session is the type of the database session object. It indicates that this dependency will provide a SQLAlchemy Session.'''


'''Depends(get_db):- is a FastAPI utility that indicates that the get_db function should be used to provide the dependency.'''


'''Annotated[Session, Depends(get_db)] essentially tells FastAPI that whenever a route handler declares this dependency, FastAPI should call get_db to get a database session and inject it into the handler.'''


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):

    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        # hashed_password = create_user_request.password,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True,
        phone_number = create_user_request.phone_number
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}