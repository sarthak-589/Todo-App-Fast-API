# from sqlalchemy import StaticPool, create_engine
# import sqlalchemy
# from routers.todos import get_db, get_current_user
# from database import Base
# from sqlalchemy.orm import sessionmaker
# from fastapi.testclient import TestClient
from fastapi import status
from .utils import *
import pytest
# from models import Todos, Users



#<-------------------------------------Tests Starts From Here-------------------------------->
# Test 1
def test_read_all_authenticated():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK



# Test 2
def  test_read_one_authenticated_not_found():
    response = client.get("/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}



# Test 3
def test_create_todo():
    response = client.post(
        "/todo",
        json={"title": "Test Todo", "description": "Test Description", "priority": 3, "complete": False}
    )
    assert response.status_code == status.HTTP_201_CREATED


# Test 4
def test_read_all_todos():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    todos = response.json()
    assert isinstance(todos, list)
    assert len(todos) > 0


# Test 5
def test_read_single_todo():
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    todo = response.json()
    assert todo['title'] == "Test Todo"
    assert todo['description'] == "Test Description"


# Test 6
def test_update_todo():
    response = client.put(
        "/todo/1",
        json={"title": "Updated Todo", "description": "Updated Description", "priority": 2, "complete": True}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify the update
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    todo = response.json()
    assert todo['title'] == "Updated Todo"
    assert todo['description'] == "Updated Description"
    assert todo['priority'] == 2
    assert todo['complete'] is True

# Test 7
def test_update_todo_not_found():
    response = client.put(
        "/todo/999",
        json={'title': "Updated Todo", "description": "Updated Description", "priority": 2, "complete": True}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND



# Test 8
def test_delete_todo():
    response = client.delete("/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify the deletion
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND