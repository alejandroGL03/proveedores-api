from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

#os.environ para despliegue. Descomente cuando ya probó todo local.
#client = MongoClient(os.environ["MONGO_URI"])
client = MongoClient("mongodb://ISIS2304H07202610:qNfD8OfLyRFM@157.253.236.88:8087")
db = client["ISIS2304H07202610"]

#endpoints
@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    comentarios = list(db.comentarios.find({"bar_id": bar_id}, {"_id": 0})) 
    
    return comentarios

@app.post('/bares/{bar_id}/comentarios')#saca datos
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha']  = datetime.now().isoformat()

    db.comentarios.insert_one(datos)
    return {'mensaje': 'Comentario guardado'}

# TODO: implementar GET /bares/{bar_id}/eventos
# Debe retornar todos los eventos del bar desde la colección 'eventos'
@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    # Buscamos en la colección 'eventos'
    eventos = list(db.eventos.find({"bar_id": bar_id}, {"_id": 0}))
    return eventos

# TODO: implementar POST /bares/{bar_id}/eventos  
# Debe insertar el evento en la colección 'eventos'
# Recuerde agregar bar_id y fecha_creacion al documento antes de insertar
@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    # Agregamos los campos requeridos al diccionario
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    
    # Insertamos en la colección 'eventos'
    db.eventos.insert_one(datos)
    
    return {'mensaje': 'Evento guardado exitosamente'}