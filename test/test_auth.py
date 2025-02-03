from .utils import *
from app.routers.auth import get_db, authenticateUser, createAccessToken, SECRET_KEY, ALGORITHM, getCurrentUser
from datetime import timedelta
from jose import jwt
from fastapi import HTTPException

# validaremos la funcion de auntenticacion de usuario
def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    # validamos si el usuario esta autenticado
    authenticate_user = authenticateUser(test_user.userName, "josejavier14", db)
    assert authenticate_user is not None
    assert authenticate_user.userName == test_user.userName

    # validamos cuando el usuario no ingresa una acontrasenia que no existe
    non_authenticate_user = authenticateUser(test_user.userName, "WrongPassword", db)
    assert non_authenticate_user is False

    # validamos cuando el usuario ingresa un usuario que no existe
    wrongUser_authenticate_user = authenticateUser("wrongUser", "josejavier14", db)
    assert wrongUser_authenticate_user is False


def test_create_accsses_token():
    # agregamos los datos que contendra el token 
    userName = 'javierha'
    id = 1
    role = "user"
    expiresDelta = timedelta(days=1)

    # creamos el token jwt
    token = createAccessToken(userName, id, role, expiresDelta)
    
    # creamnos el decodificador
    decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], 
                        options={'verify_signature': False})
    
    # validamos la decodificacion
    assert decode['sub'] == userName
    assert decode['id'] == id
    assert decode['role'] == role


# testeamos funciones asincronicas
@pytest.mark.asyncio
async def test_getCurrent_user():

    encode = {'sub': 'javierha', 'id':1, 'role':'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await getCurrentUser(token=token) # usamos await ya qye es una funcion asincronica
    # validamos el usuario
    assert user == {'username': 'javierha', 'id': 1, 'role':'admin'}

# testeamos el fallo de una funcion asincronica
@pytest.mark.asyncio
async def test_getCurrent_user_missing_payload():
    encode = {'role':'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    # declaramos un proceso
    with pytest.raises(HTTPException) as exc_info:
        await getCurrentUser(token=token)
    
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "User not validated"