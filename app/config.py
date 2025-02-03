# creamos el archivo de configuracion de variables de entonor
from dotenv import load_dotenv
import os

class Settings():
    # cargamos las varables de entorno
    load_dotenv()

    def __init__(self):
        # base de datos de produccion
        DB_URL = os.getenv('DB_URL')
        POSTGRES_PASSWORD_DB = os.getenv('POSTGRES_PASSWORD_DB')
        POSTGRES_NAME_DB = os.getenv('POSTGRES_NAME_DB')
        PORT = os.getenv('PORT')
        TEST_DB_URL = os.getenv('DB_URL')

        # base de datos de prueba
        TEST_DB_URL = os.getenv('TEST_DB_URL')
        TEST_POSTGRES_PASSWORD_DB = os.getenv('TEST_POSTGRES_PASSWORD_DB')
        TEST_POSTGRES_NAME_DB = os.getenv('TEST_POSTGRES_NAME_DB')
        TEST_PORT = os.getenv('TEST_PORT')


# creamos una instancia de la clase para que pueda usar todos los metodos
settings = Settings()
