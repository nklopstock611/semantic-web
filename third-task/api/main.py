from fastapi import FastAPI
import db

app = FastAPI()
<<<<<<< HEAD
=======
# fastapi dev main.py
>>>>>>> 34abe46 (db y eso)

@app.get('/')
def home():
    return {'hello, world!'}

@app.get('/by_keyword/{keyword}')
def get_pdfs_from_keyword(keyword: str):
    pdfs = db.get_pdfs_from_keyword(keyword)
    return pdfs
