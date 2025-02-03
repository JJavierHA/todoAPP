from typing import Annotated # sirve para declarar dependencias
from sqlalchemy.orm import Session # sirve para crear sesiones en las bases de datos
from fastapi import APIRouter, Depends, Path, HTTPException # Depends sirve para la inyeccion de dependencias
from ..models import Todos
from ..database import sesionLocal # importamos el motor de la base de datos
from starlette import status
# importamos el modulo de autenticacion con nuestro usuario para usar los metodos HTTp
from .auth import getCurrentUser # desempaquetar el token

router = APIRouter(
    prefix='/admin',
    tags=['admin']
) # creamos una instancia de FastAPI

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

#! creamos las funciones que puede hacer un usuario de tipo adminstrador 
@router.get('/todos', status_code=status.HTTP_200_OK)
async def readAllTodos(user: user_dependency, bd: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail="Authtenticated fail.")
    return bd.query(Todos).all()

@router.delete('/deleteTodo/{todoId}', status_code=status.HTTP_204_NO_CONTENT)
async def deleteTodo(user: user_dependency, db: db_dependency, todoId: int):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authenticated fail.')
    todo = db.query(Todos).filter(Todos.id == todoId).first()
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todoId).delete()
    db.commit() # guardamos los cambios en la base de datos