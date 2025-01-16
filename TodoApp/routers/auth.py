from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from models import Users
from starlette import status
from passlib.context import CryptContext # modulo para la encriptacion
# importamos lo relacionado a la base de datos
from database import sesionLocal
from typing import Annotated # permite crear/asignar dependencias
from sqlalchemy.orm import Session
# uso de formularios para la creacion de tokens
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# creacion del token JWT
from jose import jwt, JWTError # necesita un secreto y un algoritmo
from datetime import timedelta, datetime, timezone

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# AGREGARAN SEGURIDAD AL JWT
SECRET_KEY = '008c0480f29c43c49961f2fb0571b462' # creamos un codigo aleatorio con openssl rand -hex <tamanio en num>
ALGORITHM = 'HS256'

# creamo una instancia de passlib la cual permititra crear un hash de nuesta contraseña
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
# creamos una dependencia para validaciones de tokens
oauth2Bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

# creamoas una funcion para autenticar usuarios
def authenticateUser(username: str, password: str, db):
    user = db.query(Users).filter(Users.userName == username).first()
    if not user: # verificamos que el usuario exista
        return False
    if not bcrypt_context.verify(password, user.hashedPassword): # verificamos que la contraseña exista
        return False
    return user

def createAccessToken(username: str, userId: int, expiresDelta: timedelta):
    # asignamos el payload del jwt
    encode = {'sub': username, 'id': userId}
    # definimos el tiempo de vida del token para que este pueda caducar
    expires = datetime.now(timezone.utc) + expiresDelta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

#creamos una clase para la validacion 
class UserRequest(BaseModel):
    
    userName: str
    email: str
    firstName: str
    lastName: str
    password: str
    role: str

class Token(BaseModel):
    accessToken: str
    tokenType: str

#! crearemos nuestra funcion de dependencias
def get_db():
    db = sesionLocal()
    try:
        yield db
    finally:
        db.close()

# creamos nuestra inyeccion de dependencia
db_dependency = Annotated[Session, Depends(get_db)] # asignamos el tipo, asigamos la funcion dependiente

# creamos una funcion que permitira validar el token jwt
async def getCurrentUser(token: Annotated[str, Depends(oauth2Bearer)]):
    # trataremos de obtener el payload de un token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        userId: str = payload.get('id')
        if username is None or userId is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail='User not validated')
        return {'username': username, 'id': userId}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='User not validated')

#! Funcion POST
@router.post("/", status_code=status.HTTP_201_CREATED)
async def creatUser(db: db_dependency ,userRequest: UserRequest):
    newUser = Users(
        userName = userRequest.userName,
        email = userRequest.email,
        firstName = userRequest.firstName,
        lastName = userRequest.lastName,
        hashedPassword = bcrypt_context.hash(userRequest.password), # creamos el hash de nuestra contrasenia
        role = userRequest.role
    )
    db.add(newUser)
    db.commit()

@router.post("/token", response_model=Token) # especificamos el modelo de respuesta echo con pydantic
async def loginForAccessToken(dataForm: Annotated[OAuth2PasswordRequestForm, Depends()],
                              db: db_dependency):
    user = authenticateUser(dataForm.username, dataForm.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail='User not validated')
    token = createAccessToken(user.userName, user.id, timedelta(minutes=20))
    return {'accessToken': token, 'tokenType': 'bearer'} # segimos la estructura del modelo de respuesta establecido

#* es importante hasear las contrasenias almacenadas con la finalidad de que en 
#* dado caso de algun vulnerabilidad este pueda tener un nivel de seguriad y no
# * se almacene en texto plano