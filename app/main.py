from fastapi import FastAPI 
from . import models
from .database import engine # importamos el motor de la base de datos
from .routers import auth, todos, admin, user # importacion de los routers

app = FastAPI() # creamos una instancia de FastAPI

# creamos la base de datos dentro de nuestro archivo principal para instanciar 
# el modelo dentro de la BD
models.base.metadata.create_all(bind=engine)

# Funcion que determina el estado de la api
@app.get("/health")
def healthCheck():
    return {'status': 'healthy'}

# hacemos la importacion de los roouters
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(user.router)
app.include_router(admin.router)