from typing import Annotated # sirve para declarar dependencias
from sqlalchemy.orm import Session # sirve para crear sesiones en las bases de datos
from fastapi import APIRouter, Depends, Path, HTTPException # Depends sirve para la inyeccion de dependencias
from models import Todos
from database import sesionLocal # importamos el motor de la base de datos
from starlette import status
from pydantic import BaseModel, Field

router = APIRouter() # creamos una instancia de FastAPI

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

#* agregamos validaciones a los endpoint generados
#! Funcion GET
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@router.get("/todo/{todoId}", status_code=status.HTTP_200_OK)
async def readTodo(db: db_dependency, todoId: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == todoId).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=404, detail="Todo not found.")

#! Funcion POST
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def creatTodo(db: db_dependency, todoRequest: TodoRequest):
    todo = Todos(**todoRequest.model_dump()) # creamos un objeto del modelo Todos
    db.add(todo) # agregamos a la base de datos el objto
    db.commit() # aplicamos los cambios manualmente

#! Funcion PUT
@router.put("/updateTodo/{todoId}", status_code=status.HTTP_204_NO_CONTENT)
async def updateTodo(db: db_dependency, 
                    todoReques: TodoRequest, 
                    todoId: int = Path(gt=0)):
    # realizamos un filtro para encontrar el elemento
    todo = db.query(Todos).filter(Todos.id == todoId).first()

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
async def deleteTodo(db: db_dependency, todoId: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == todoId).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    db.query(Todos).filter(Todos.id == todoId).delete() # filtramos el elemento y eliminamos

    db.commit() # realizamos la transaccion manualmente