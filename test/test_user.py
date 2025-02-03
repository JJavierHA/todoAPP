from .utils import *
from app.routers.user import get_db, getCurrentUser
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[override_getCurrentUser] = override_getCurrentUser

def test_get_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    db = TestingSessionLocal()

    assert response.json()['userName'] == 'javierha'
    assert bcrypt_context.verify("josejavier14", response.json()['hashedPassword'])

def test_change_password(test_user):
    request_data = {
        'oldPassword': 'josejavier14',
        'newpassword': 'josejose14'
    }
    response = client.put("/user/changePassword", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()
    assert bcrypt_context.verify(request_data.get('newpassword'), model.hashedPassword)

def test_change_password_invalid(test_user):
    request_data = {
        'oldPassword': 'javier',
        'newpassword': 'josejose14'
    }
    response = client.put("/user/changePassword", json=request_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': "Passwords don't match."}


def test_change_phone(test_user):
    response = client.put("/user/changePhone", json={'phone': "1234567890"})

    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()
    assert model.phone == "1234567890"