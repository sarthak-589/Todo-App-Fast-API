from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from database import Base
from models import Users, Todos
from routers.todos import get_db, get_current_user
from routers.auth import bcrypt_context
import pytest


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost:5432/test_db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'sarthak_123', 'id': 1, 'user_role': 'admin'}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Create test user
    db = TestingSessionLocal()
    try:    
        user = Users(id=1, email="sarthak123@gmail.com", username="sarthak_123", first_name="Sarthak", last_name="Shah", hashed_password="testpassword", is_active=True, role="admin", phone_number="1234567890")
        db.add(user)
        db.commit()
    finally:
        db.close()

    yield      # This allows the tests to run

    
    # Drop the tables after the tests are complete
    db = TestingSessionLocal()  # Create a session object
    try:
        Base.metadata.drop_all(bind=engine)
    finally:
        db.close()


# @pytest.fixture(scope="module", autouse=True)
# def setup_database():
#     yield
#     # Drop the tables after the tests are complete
#     db = TestingSessionLocal()  # Create a session object         
#     try:
#         Base.metadata.drop_all(bind=engine)
#     finally:
#         db.close()


@pytest.fixture
def test_todo():
    db = TestingSessionLocal()
    try:
        todo = Todos(title="Test Todo", description="Test Description", priority=3, complete=False, owner_id=1)
        db.add(todo)
        db.commit()
    finally:
        db.close()
    yield
    
    # Optionally, cleanup after the test
    db = TestingSessionLocal()
    try:
        db.query(Todos).filter(Todos.id == 1).delete()
        db.commit()
    finally:
        db.close()



@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    try:
        user = Users(
            id=1,
            username="sarthak_123",
            email="sarthak123@gmail.com",
            first_name="Sarthak",
            last_name="Shah",
            hashed_password=bcrypt_context.hash("python@123"),
            is_active=True,
            role="admin",
            phone_number="8898424255"
        )
        db.add(user)
        db.commit()
    finally:
        db.close()
    yield user
    
    # Teardown: remove the user after the test
    db = TestingSessionLocal()
    try:
        db.query(Users).filter(Users.id == 1).delete()
        db.commit()
    finally:
        db.close()