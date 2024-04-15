import requests
import json

credentials_path = '/semantic-web/credentials.json'

with open(credentials_path) as f:
    json_obj = json.load(f)

api_key = json_obj["API_KEY_SS"]

headers = {
    'x-api-key': api_key,
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

"""
1 - Entrar al arreglo de autores
2 - Recorrer el arreglo de autores
3 - Para cada autor, verificar si está el paper objetivo
    (es decir, comparar el título del JSON con los asociados al autor)

    Caso 1 -> está el paper
        1.1 - sacar ID
        1.2 - request GET para sacar detalles del paper
        1.3 - ver si tiene el link de descarga
        1.4 - WEBSCRAPPER (o no sé):
            1.4.1 - Descargar el pdf

    Caso 2 -> no está el paper
        1.1 - acaba el proceso y sigue al otro autor
"""

def verify_status_and_return(response, data: int=0):
    """
    Verifies the status of the response and returns the data
    if it's a 200 status code.
    """
    if response.status_code == 200:
        ret = json.dumps(response.json(), indent=2)
        ret = json.loads(ret)
        if data == 0:
            return ret
        elif data == 1:
            return ret['data']
        elif data == 2:
            return ret['data'][0]
    else:
        print(f"Error: {response.status_code}")
        print(json.dumps(response.json(), indent=2))

def get_papers_from_author(author_name: tuple) -> dict:
    """
    Returns the papers of the author in JSON format.

    Author object (relevant fields):
    {..., "data": [
                    "authorId": "1741101",
                    "name": "Oren Etzioni",
                    "papers": [],
                  ]
    }
    """
    url = f'https://api.semanticscholar.org/graph/v1/author/search?query={author_name[0]}+{author_name[1]}'
    response = requests.get(
        url,
        headers=headers,
        params={
            "fields": 'name,papers.title,papers.year',
        }
    )

    return verify_status_and_return(response, True)

def find_paper(paper_title: str) -> dict:
    """
    Returns the details of the paper in JSON format.    
    """
    query_params = {'query': paper_title,
                    "fields": "corpusId,title,year,referenceCount,citationCount,influentialCitationCount,isOpenAccess,openAccessPdf,publicationDate"
    }
    url = f'https://api.semanticscholar.org/graph/v1/paper/search/'
    response = requests.get(
        url,
        headers=headers,
        params=query_params
    )

    if response.status_code == 200:
        ret = json.dumps(response.json(), indent=2)
        ret = json.loads(ret)
        try:
            return ret['data'][0]
        except KeyError:
            print('Error: No "data" key')
    else:
        print(f"Error: {response.status_code}")
        print(json.dumps(response.json(), indent=2))

def get_paper(paper_id: str):
    """
    Returns the details of the paper in JSON format.

    Paper object (relevant fields):
    {
        "paperId": "649def34f8be52c8b66281af98ae884c09aef38b",
        "corpusId": 2314124,
        "title": "Construction of the Literature Graph in Semantic Scholar",
        "year": 2018,
        "referenceCount": 321,
        "citationCount": 987,
        "influentialCitationCount": 654,
        "isOpenAccess": true,
        "openAccessPdf": {},
        "publicationDate": "2015-01-17",
    }
    """
    url = f'https://api.semanticscholar.org/graph/v1/paper/{paper_id}'
    response = requests.get(
        url,
        headers=headers,
        params={
            "fields": "corpusId,title,year,referenceCount,citationCount,influentialCitationCount,isOpenAccess,openAccessPdf,publicationDate"
        }
    )

    return verify_status_and_return(response)

def get_pdf(paper_link: str):
    """
    Returns the url to the paper pdf.
    """
    try:
        response = requests.get(paper_link, timeout=60)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el PDF: {e}")
        return None
