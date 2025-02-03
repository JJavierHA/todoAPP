from .utils import *
from app.routers.admin import get_db, getCurrentUser
from fastapi import status
from app.models import Todos

# sobre escribimos las dependencias
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[getCurrentUser] = override_getCurrentUser

def test_get_all_todos(test_todo):
    response = client.get("/admin/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "title": "Verbos HTTP",
        "description": "Prueba de fastapi",
        "priority": 5,
        "complete": False,
        "owner": 1,
    }]

def test_delete_todos(test_todo):
    response = client.delete("/admin/deleteTodo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todos_not_found():
    response = client.delete("/admin/deleteTodo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}