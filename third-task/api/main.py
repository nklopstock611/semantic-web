import db
import pdf_processor as pp

import json
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las fuentes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los headers
)

@app.get('/')
def home():
    return {'hello, world!'}

@app.get('/by_keyword/{keyword}')
def get_pdfs_from_keyword(keyword: str):
    pdfs = db.get_pdfs_from_keyword(keyword)
    return pdfs

@app.get('/by_paper/{paper}')
def get_authors_from_paper(paper: str):
    authors = db.get_authors_from_paper(paper)
    return authors

@app.post('/add_pdf')
async def add_pdf(file: UploadFile = File(...)):
    try:
        print('Got PDF:', file.filename)
        parsed_article = await pp.parse_pdf(file)
        metadata = pp.xml_query(parsed_article, file.filename)
        # print('Metadata:', metadata)
        return JSONResponse(content=metadata)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post('/insert_data')
async def insert_data(data: dict):
    try:
        success = db.insert_triple(data)
        if success:
            return JSONResponse(content={"message": "Data inserted successfully"}, status_code=200)
        else:
            raise ValueError("Failed to insert data due to validation failure or other non-exceptional issue.")
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

"""
Pasos:
- Definir Shapes (CHECK)
- Recibir el PDF (CHECK)
- Guardar el PDF (MÁS O MENOS... SE GUARDA LOCAL PERO NO EN DRIVE NI NADA...)
- Pasarlo por GROBID (CHECK)
- Sacar la metadata en un JSON por cada solicitud (CHECK)
- Mostrar el resultado que saca GROBID en un
  espacio de intefaz gráfica (CHECK)
- Dejar al usuario poder ver lo que sacó GROBID
  y poder corregirlo si desea (CHECK)
- Cuando esté listo, se crea el grafo con la información (CHECK)
- Se verifica con los Shapes (CHECK)
    - En caso de que pase todo correctamente, se guardan las tuplas
        - Se muestra un mensaje de éxito
    - En caso de que falle, se muestra un mensaje de error (CHECK)
"""