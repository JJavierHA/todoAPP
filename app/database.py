# vamos a generar una coneccion con el ORM SQLAlchemy
# este archivo permitira conectar el ORM con la base de datos
##* crearemos una instacia de incio de secion local lo que permitira convertirse en una BD
from sqlalchemy import create_engine # creara un motor para la coneccion con la base de datos
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

#! conexion con sqlite3
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosApp.db' # creamos la ruta donde se generara la base de datos
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

#! coneccion con postgreSQL
SQLALCHEMY_DATABASE_URL = settings.DB_URL # importamos el valor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

sesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # generamos una sesion local

base = declarative_base() # creamos una declaracion de la base de datos que va a ser capas de manejar la BD
