# creamos el archivo de configuracion de variables de entonor
from dotenv import load_dotenv
import os
from pathlib import Path

class Settings():
    # accedemos a la ruta de larchivo
    BASE_DIR = Path(__file__).resolve().parent.parent
    ENV_PATH = BASE_DIR / ".env"
    # cargamos las varables de entorno
    load_dotenv(ENV_PATH)

    def __init__(self):
        # base de datos de produccion
        self.DB_URL = os.getenv('DB_URL')
        self.POSTGRES_PASSWORD_DB = os.getenv('POSTGRES_PASSWORD_DB')
        self.POSTGRES_NAME_DB = os.getenv('POSTGRES_NAME_DB')
        self.PORT = os.getenv('PORT')
        self.TEST_DB_URL = os.getenv('DB_URL')

        # base de datos de prueba
        self.TEST_DB_URL = os.getenv('TEST_DB_URL')
        self.TEST_POSTGRES_PASSWORD_DB = os.getenv('TEST_POSTGRES_PASSWORD_DB')
        self.TEST_POSTGRES_NAME_DB = os.getenv('TEST_POSTGRES_NAME_DB')
        self.TEST_PORT = os.getenv('TEST_PORT')


# creamos una instancia de la clase para que pueda usar todos los metodos
settings = Settings()
