from typing import Annotated # sirve para declarar dependencias
from sqlalchemy.orm import Session # sirve para crear sesiones en las bases de datos
from fastapi import APIRouter, Depends, Path, HTTPException # Depends sirve para la inyeccion de dependencias
from models import Todos
from database import sesionLocal # importamos el motor de la base de datos
from starlette import status
from pydantic import BaseModel, Field
# importamos el modulo de autenticacion con nuestro usuario para usar los metodos HTTp
from .auth import getCurrentUser # desempaquetar el token

router = APIRouter(
    tags=["Todos"]
) # creamos una instancia de FastAPI

#! creamos el modelo request de nuesto modelo Alchemy
class TodoRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=200)
    priority: int = Field(gt=0, lt=6)
    complete: bool

# crearemos una funcion de dependencia 
# permitira crear una sesion temporal la cual durara mientras se ejecute dentro 
# de una funcion gracias a la injecion dependencias
# proporciona acceso controlado a la base de datos
def get_db():
    db = sesionLocal() # creamos una sesion local temporal importando la sesion desde database.py
    # trataremos de ejecutar esta sesion y en cuanto finalice serraremos la sesion
    try: 
        # permite a la función que la consuma usar la sesión.
        yield db # Se cede el control al contexto que llame a esta función
    finally:
        db.close()
# especificamos el tipo de dato que se espera recibir
# especificamos que esta variable depende de la funcion get
db_dependency = Annotated[Session, Depends(get_db)] # creamos una variable que indica la dependencia de la conexion 
# creamos una inyeccion de dependencias para nuestras funciones HTTP
user_dependency = Annotated[dict, Depends(getCurrentUser)]

#* agregamos validaciones a los endpoint generados
#! Funcion GET
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency, db: db_dependency):
    if user is None:
        HTTPException(status_code=401, detail="Authenticated fail.")
    return db.query(Todos).filter(Todos.owner == user.get('id')).all()

@router.get("/todo/{todoId}", status_code=status.HTTP_200_OK)
async def readTodo(user:user_dependency, db: db_dependency, 
                   todoId: int = Path(gt=0)):
    if user is None:
        HTTPException(status_code=401, detail="Authenticated fail.")

    todo = db.query(Todos).filter(Todos.id == todoId)\
        .filter(Todos.owner == user.get('id')).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=404, detail="Todo not found.")

#! Funcion POST
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def creatTodo(user: user_dependency, db: db_dependency, 
                    todoRequest: TodoRequest):
    if user is None:
        HTTPException(status_code=401, detail="Authenticated fail.")
    # creamos un objeto del modelo Todos y le pasamos el id del usuario autenticado
    todo = Todos(**todoRequest.model_dump(), owner=user.get('id'))
    db.add(todo) # agregamos a la base de datos el objto
    db.commit() # aplicamos los cambios manualmente

#! Funcion PUT
@router.put("/updateTodo/{todoId}", status_code=status.HTTP_204_NO_CONTENT)
async def updateTodo(user: user_dependency, db: db_dependency, 
                    todoReques: TodoRequest, 
                    todoId: int = Path(gt=0)):
    if user is None:
        HTTPException(status_code=401, detail="Authenticated fail.")
    # realizamos un filtro para encontrar el elemento
    todo = db.query(Todos).filter(Todos.id == todoId)\
        .filter(Todos.owner == user.get('id')).first()

    # validamos que se devolvio algo
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not fount.")
    
    # actualizamos los campos
    todo.title = todoReques.title
    todo.description = todoReques.description
    todo.priority = todoReques.priority
    todo.complete = todoReques.complete

    # agregamos los cambios a la Bd
    db.add(todo) # alchemy internamente sabe que debe actualir el 
    # elemento siempre y cuando sea una instancia de la query
    db.commit()

#! Funcion DELETE
@router.delete("/deleteTodo/{todoId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTodo(user: user_dependency ,db: db_dependency, 
                     todoId: int = Path(gt=0)):
    if user is None:
        HTTPException(status_code=401, detail="Authenticated fail.")

    todo = db.query(Todos).filter(Todos.id == todoId)\
        .filter(Todos.owner == user.get('id')).first()
        
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    db.query(Todos).filter(Todos.id == todoId).delete() # filtramos el elemento y eliminamos

    db.commit() # realizamos la transaccion manualmente