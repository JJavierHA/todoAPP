from fastapi.testclient import TestClient
from app import main
from fastapi import status

# creamos un cliente que podra consumir las URL de los endpoints
client = TestClient(main.app)

#* creamos las funciones de prueba
def test_return_health_check():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'healthy'}