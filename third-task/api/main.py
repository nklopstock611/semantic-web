import db
import pdf_processor as pp
import gdrive as gd

import json
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

temp_path = './temp_files'

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
    data = db.get_information_from_paper(paper)
    return data

@app.get('/recommendations/{paper}')
def get_recommendation_for_given_paper(paper: str):
    recommendations = db.get_recommendation_for_given_paper(paper)
    return recommendations

@app.get('/by_author/{author}')
def get_papers_by_author(author: str):
    papers = db.get_papers_by_author(author)
    return papers

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
        success_neo4j = db.insert_triple(data)
        paper_dict = list(data.keys())[0]
        success_drive = gd.save_pdf_drive(f"{temp_path}/{data[paper_dict]['paper_downloaded_pdf']}", data[paper_dict]['paper_downloaded_pdf'])
        if success_neo4j and success_drive:
            return JSONResponse(content={"message": "Data inserted successfully"}, status_code=200)
        else:
            raise ValueError("Failed to insert data due to validation failure or other non-exceptional issue.")
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get('/download_pdf/{file_name}')
def download_pdf(file_name: str):
    try:
        print('File name:', file_name)
        file_name = file_name.replace('"', '%2')
        print('File name:', file_name)
        pdf_content, suggested_filename = gd.download_pdf_drive(file_name)
        if pdf_content is None:
            raise HTTPException(status_code=404, detail="File not found")
        
        headers = {
            "Content-Disposition": f"attachment; filename={suggested_filename}"
        }
        
        return StreamingResponse(pdf_content, media_type="application/pdf", headers=headers)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(content={"error": str(e) + '\n No se encontró el archivo.'}, status_code=500)

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
        - Se muestra un mensaje de éxito (CHECK)
    - En caso de que falle, se muestra un mensaje de error (CHECK)
    
CONSULTAS:
- Papers de un mismo autor
- Papers que comparten keywords:
    - ver los keywords de un paper dado
    - ver los papers que comparten keywords
    - mostrar solo los que comparten más keywords
- Información de un paper dado
    - Título
    - Año de publicación
    - Abstract
    - Autores (juntando nombre y apellido)
    - Botón para descargar el PDF
"""