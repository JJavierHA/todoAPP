from app.main import app
# importamos las variables de entorno
from app.config import settings
# imporamos lo relacionado a la base de datos
from sqlalchemy import create_engine, text
from app.routers.auth import bcrypt_context
from sqlalchemy.pool import StaticPool # permite mantener una misma conexion
from sqlalchemy.orm import sessionmaker
from app.database import base

from app.models import Todos, Users
import pytest

from fastapi.testclient import TestClient

# Crearemos todo lo relacionado a la conecxion con la base de datos
TEST_DB_URL = settings.TEST_DB_URL

engine = create_engine(TEST_DB_URL, poolclass=StaticPool) # creamos el motor de la base de datos

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# creamos nuestra base de datos
base.metadata.create_all(bind=engine)

# sobre escribimos la dependencia por un nueva que tendra la conexion con la base de datos
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_getCurrentUser():
    return {'username': "javierha", 'id': 1, 'role':"admin"}

client = TestClient(app)

# creamos un fixture que devolvera un todo, lo eleminara y sera validado pos los test
@pytest.fixture
def test_todo(test_user):
    todo = Todos(
        title = "Verbos HTTP",
        description = "Prueba de fastapi",
        priority = 5,
        complete = False,
        owner = 1,
    )
    # guardamos los cambios
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    # lanzamos el todo como parametro
    yield todo
    # abrimos un proceso que solo durara mientras se raliza la conexion
    # eliminara los elementos de tabla y se cerrara automaticamente
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.execute(text("ALTER SEQUENCE todos_id_seq RESTART WITH 1")) #! Reiniciamos la secuencia unicamente para base postgreSQL
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        email = "example@gmail.com",
        userName = "javierha",
        firstName = "jose javier",
        lastName = "Herrera",
        hashedPassword = bcrypt_context.hash("josejavier14"),
        isActive = True,
        role = "admin",
        phone = "9631892525"
    )
    # almacenamos el usuario
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    # lanzamos el elemento
    yield user
    # finalizamos el proceso
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1"))
        connection.commit()


