import requests
import json

with open('./credentials.json') as f:
    json_obj = json.load(f)

api_key = json_obj["API_KEY_SS"]

headers = {'x-api-key': api_key}

def get_papers_from_author(author_name: tuple) -> dict:
    url = f'https://api.semanticscholar.org/graph/v1/author/search?query={author_name[0]}+{author_name[1]}'
    print(url)
    response = requests.get(
        url,
        headers=headers,
        params={
            "fields": 'name,papers.title,papers.year',
            # "limit": 1
        }
    )

    if response.status_code == 200:
        ret = json.dumps(response.json(), indent=2)
        ret = json.loads(ret)
        return ret['data']
    else:
        print(f"Error: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return None

# get_papers_from_author(('a', 'descamps'))

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