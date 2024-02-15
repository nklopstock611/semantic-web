import requests
import json

with open('./credentials.json') as f:
    json_obj = json.load(f)

api_key = json_obj["API_KEY_SS"]

headers = {'x-api-key': api_key}

def verify_status_and_return(response, data: bool=False):
    """
    Verifies the status of the response and returns the data
    if it's a 200 status code.
    """
    if response.status_code == 200:
        ret = json.dumps(response.json(), indent=2)
        ret = json.loads(ret)
        if not data:
            return ret
        else:
            return ret['data']
    else:
        print(f"Error: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return None

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
            # "limit": 1
        }
    )

    return verify_status_and_return(response, True)

# print(get_papers_from_author(('m', 'atiquzzaman')))

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
    # TO-DO: tal vez volver todo esto en una misma función grande y que sea solo pasar parámetros
    url = f'https://api.semanticscholar.org/graph/v1/paper/{paper_id}'
    response = requests.get(
        url,
        headers=headers,
        params={
            "fields": "corpusId,title,year,referenceCount,citationCount,influentialCitationCount,isOpenAccess,openAccessPdf,publicationDate"
        }
    )

    return verify_status_and_return(response)

# print(get_paper('59a0dabcfa4e8d8fe4a7e539413b4239c9bee631'))  

def get_pdf(paper_link: str):
    """
    Returns the url to the paper pdf.
    """
    response = requests.get(paper_link)
    return response

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

De pronto ayuda hacer THREADS? un thread para cada autor? -> me da cosa el tema de número de request... 5k cada 5 mins...
"""
