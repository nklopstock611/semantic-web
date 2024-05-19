import os
import io
import tempfile
from fastapi import HTTPException
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

gauth = GoogleAuth()
gauth.LoadCredentialsFile("credentials.json")

if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

# gauth.SaveCredentialsFile("credentials.json")
drive = GoogleDrive(gauth)

folder_id = '1uYpMPOGJZaOeAxQ-Ply22AGJA5iGnSxD'

def save_pdf_drive(ruta_archivo_local, nombre_archivo, id_carpeta=folder_id):
    try:
        archivo = drive.CreateFile({
            'title': nombre_archivo,
            'parents': [{'id': id_carpeta}]
        })
        archivo.SetContentFile(ruta_archivo_local)
        archivo.Upload()
        print(f'Archivo {nombre_archivo} guardado en Google Drive.')
        return True
    except Exception as e:
        print(f'Ocurrió un error al guardar el archivo: {e}')
        return False

def download_pdf_drive(file_name: str):
    try:
        # Search for the file by name
        file_list = drive.ListFile({'q': f"title = '{file_name}' and mimeType = 'application/pdf' and trashed=false"}).GetList()

        if not file_list:
            print("No file found.")
            return None
        
        # Assuming you want to download the first file found with that name
        file = file_list[0]
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.GetContentFile(temp_file.name, mimetype='application/pdf')

            # Read the content from the temporary file into BytesIO
            temp_file.seek(0)
            file_io = io.BytesIO(temp_file.read())
            file_io.seek(0)

        # Optionally, delete the temporary file if you do not want it to persist
        os.remove(temp_file.name)
        
        return file_io, file_name
    except Exception as e:
        print(f"Failed to download file: {str(e)} File not found.")
        raise e
