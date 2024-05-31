from urllib import response
from fastapi import status
from .utils import *
import pytest
from routers.admin import get_db, get_current_user


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(setup_database, test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    todos = response.json()
    assert isinstance(todos, list)
    assert len(todos) > 0