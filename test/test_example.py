import pytest

# es importante especificar test_ antes de cada funcion de prueba para que esta sea reconocida
# al igua que tienen que estar en un directorio "test" en un archivo llamado "test_" 
def test_is_equals():
    assert 3 == 3 

def test_is_instance():
    assert isinstance("hola", str)

def test_isBolean():
    assert True
    assert 7 > 3

def test_tipe():
    assert ("hola" == "hola") is True
    assert type("hola" is str)

def test_list():
    nums = [1,2,3,4]
    anyList =[ False, False]
    assert 1 in nums
    assert 7 not in nums
    assert all(nums)
    assert not any(anyList)


# Prueba de objetos
class Estudent:
    def __init__(self, firtsName, lastName, major, years):
        self.firtsName = firtsName
        self.lastName = lastName
        self.major = major
        self.years = years


# creamos un elemento global que sera usado por las demas funciones de prueba
# esto evitara tener que repetir codigo continuamente
@pytest.fixture
def defaultPerson():
    return Estudent("Javier", "Herrera", "Ing. en sistemas", 4)


def test_person_initialization(defaultPerson):
    assert defaultPerson.firtsName == "Javier", "El nombre debe ser javier"
    assert defaultPerson.lastName == "Herrera", "El apellido deve ser Herrera"
    assert defaultPerson.major == "Ing. en sistemas"
    assert defaultPerson.years == 4

    