from typing import Annotated # sirve para declarar dependencias
from sqlalchemy.orm import Session # sirve para crear sesiones en las bases de datos
from fastapi import APIRouter, Depends, Path, HTTPException # Depends sirve para la inyeccion de dependencias
from models import Users
from database import sesionLocal # importamos el motor de la base de datos
from starlette import status
from pydantic import BaseModel
# importamos el modulo de autenticacion con nuestro usuario para usar los metodos HTTp
from .auth import getCurrentUser # desempaquetar el token
from passlib.context import CryptContext # modulo para la encriptacion

router = APIRouter(
    prefix='/user',
    tags=['user']
) # creamos una instancia de FastAPI

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
# creamo una instancia de passlib la cual permititra crear un hash de nuesta contraseña
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class ChangePasswordRequest(BaseModel):
    oldPassword: str
    newpassword: str

#! creamos las funciones que puede hacer un usuario de tipo adminstrador 
@router.get('/', status_code=status.HTTP_200_OK)
async def getUser(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authenticated fail.")
    # Todo: mostrar solo los datos necesarios
    return db.query(Users).filter(Users.id == user.get('id')).first()

# funcion para cambiar la contrasela del usuario autenticado
@router.put('/changePassword', status_code=status.HTTP_204_NO_CONTENT)
async def changePassword(user: user_dependency, db: db_dependency, 
                         passwordRquest: ChangePasswordRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authenticated fail.")
    
    user = db.query(Users).filter(Users.id == user.get('id')).first()
    
    # actualizamos los datos del elemento
    if not bcrypt_context.verify(passwordRquest.oldPassword, user.hashedPassword):
        raise HTTPException(status_code=401, detail="Passwords don't match.")
    user.hashedPassword = bcrypt_context.hash(passwordRquest.newpassword)
    # guardamos los cambios
    db.add(user)
    db.commit()
