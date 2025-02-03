from app.routers.todos import get_db, getCurrentUser # importamos la dependencia que queremos sobre escribir
from app.models import Todos

# importamos lo relacionado con la prueba
from fastapi import status

# importamos las utilidades
from .utils import *

# sobre escribimos la dependencia de la app con esta para que pueda usar la 
# conexion con la base de datos de prueba
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[getCurrentUser] = override_getCurrentUser

# testeamos las funciones de todos.py
# pasamos el valor a la funcion como el cuerpo del metodo GET
def test_read_all(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "title": "Verbos HTTP",
        "description":"Prueba de fastapi",
        "priority": 5,
        "complete": False,
        "owner": 1,
    }]


def test_read_one_not_found(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title": "Verbos HTTP",
        "description":"Prueba de fastapi",
        "priority": 5,
        "complete": False,
        "owner": 1,
    }

def test_read_one():
    response = client.get("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'Todo not found.'}

def test_creatTodo(test_todo):
    request_data = {
        "title": "New Todo",
        "description":"new todo made",
        "priority": 4,
        "complete": False,
        "owner": 1,
    }

    response = client.post("/todo", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED # el servidor devuelve un 201_ok
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    #* es importante validar que los de mas datos se esten guardando correctamente

def test_update_todo(test_todo):
    
    request_data = {
        "title": "update todo",
        "description":"update todo!",
        "priority": 4,
        "complete": True,
        "owner": 1,
    }

    response = client.put("/updateTodo/1", json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "update todo"
    assert model.complete == True

def test_update_todo_not_found():
    request_data = {
        "title": "update todo",
        "description":"update todo!",
        "priority": 4,
        "complete": True,
        "owner": 1,
    }

    response = client.put("/updateTodo/999", json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail':'Todo not fount.'}

def test_delete_todo(test_todo):
    response = client.delete("/deleteTodo/1")
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert  model is None

# Nota: se crea una funcion que sera global para todas las pruebas, esta creara un elemento y sera 
# lanzado con yield para ser usada durante toda la vida de la funcion para despues volver y elimiar 
# t-odos los elementos de la base de datos para que no afecten a las demas pruebas