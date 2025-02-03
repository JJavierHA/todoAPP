from .database import base # importamos el modelo base para generar los modelos en la base de datos
from sqlalchemy import Integer, String, Boolean, Column, ForeignKey # importamos los tipos de datos y la columna

class Users(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    userName = Column(String, unique=True)
    firstName = Column(String)
    lastName = Column(String)
    hashedPassword = Column(String)
    isActive = Column(Boolean, default=True)
    role = Column(String)
    phone = Column(String) # creamos un nuevo campo

class Todos(base):
    __tablename__ = "todos" # especificamos el nombre de la tabla que generaremos
    # especificamos los campos que tendra este modelo
    id = Column(Integer, primary_key=True, index=True) # especificamos el tipo de dato, la hacemos Pk y el indexado
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner = Column(Integer, ForeignKey("users.id")) # creamos una llave foranea de usuarios
