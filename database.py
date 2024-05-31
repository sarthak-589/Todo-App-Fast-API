from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost:5432/Todos_Db'

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})   # This is connect_args is for SQLITE Database.

engine = create_engine(SQLALCHEMY_DATABASE_URL)       # This is for POSTGRESQL Database.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()