import json
import requests
import threading
from time import sleep
from typing import List

metadata_path = '/semantic-web/first-task/metadata.json'
pdf_path = '/semantic-web/first-task/pdf-downloader/spdfs/'
cache_path = '/semantic-web/first-task/pdf-downloader/cache.txt'

lock = threading.Lock()

with open('./credentials.json') as f:
    json_obj = json.load(f)

api_key = json_obj["API_KEY_SS"]

headers = {
    'x-api-key': api_key,
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

with open(metadata_path) as f:
    metadata = json.load(f)

def get_references(paper: dict) -> list:
    """
    Gets the references from one paper.
    """
    titles = []
    references = paper['references']
    for each_reference in references:
        if each_reference['title'].lower() not in titles and each_reference['title'].lower() != paper['title'].lower():
            titles.append(each_reference['title'])
            
    return titles

def find_paper_and_append_id(paper_title: str, ids: List[str], headers: dict):
    """
    Requests the paper, if found, appends the ID to a list of ids.
    This functino is used to find the papers from a references list.
    """
    query_params = {
        'query': paper_title,
        "fields": "corpusId,title,year,referenceCount,citationCount,influentialCitationCount,isOpenAccess,openAccessPdf,publicationDate"
    }
    url = 'https://api.semanticscholar.org/graph/v1/paper/search/'
    response = requests.get(url, headers=headers, params=query_params)
    
    if response.status_code == 200:
        ret = json.loads(response.text)
        try:
            paper_id = ret['data'][0]['paperId']
            with lock:
                ids.append(paper_id)
                
            sleep(5)
        except KeyError:
            print('Error: No "data" key')
    else:
        print(f"Error: {response.status_code}")
        print(json.dumps(response.json(), indent=2))

def find_papers(papers_titles: List[str], headers: dict) -> List[str]:
    ids = []
    threads = []
    
    for each_paper in papers_titles:
        # Creates a thread for each paper
        thread = threading.Thread(target=find_paper_and_append_id, args=(each_paper, ids, headers))
        threads.append(thread)
        thread.start()
    
    # Waits for all threads to finish
    for thread in threads:
        thread.join()
    
    return ids

def get_papers_batch(ids: list):
    """
    Get the papers in batch.
    """
    url = 'https://api.semanticscholar.org/graph/v1/paper/batch'
    
    response = requests.post(
        url,
        headers=headers,
        params={'fields': 'paperId,title,publicationDate,venue,referenceCount,citationCount,influentialCitationCount,isOpenAccess,openAccessPdf,publicationDate'},
        json={"ids": ids}
    )

    if response.status_code == 200:
        ret = json.dumps(response.json(), indent=2)
        ret = json.loads(ret)
        for each_paper in ret:
            print(f"Paper: {each_paper['title']}")
            print(f"PDF: {each_paper['isOpenAccess']}, {each_paper['openAccessPdf']}")
            if each_paper['openAccessPdf'] != None:
                if each_paper['openAccessPdf']['url'][-4:] == '.pdf':
                    download_paper(each_paper)
                    
        sleep(5)
    else:
        print(f"Error: {response.status_code}")
        print(json.dumps(response.json(), indent=2))

def download_paper(paper: dict):
    """
    Downloads the paper from the url.
    """
    url = paper['openAccessPdf']['url']
    print(f"Downloading: {paper['title']}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"{pdf_path}{paper['paperId']}.pdf", 'wb') as f:
                f.write(response.content)
        else:
            print(f"Error: {response.status_code}")
            print(json.dumps(response.json(), indent=2))
    except requests.exceptions.ConnectionError as e:
        print("Error de conexión: No se pudo establecer una conexión con el servidor.")
    except json.JSONDecodeError:
        print("Error de JSON Decoding.")
    except requests.exceptions.TooManyRedirects:
        print("Muchos redirects")
    except requests.exceptions.ChunkedEncodingError:
        print("Chunk Encodign Error")

if __name__ == '__main__':
    with open(cache_path, 'w') as f:
        # to restart the cache for each execution...
         pass

    with open(metadata_path) as f:
        metadata = json.load(f)

    # if the download is interrupted, you can start from a specific paper
    starting_key = next((clave for clave, valor in metadata.items() if valor['title'] == "Placing Flickr Photos on a Map"), None)
    
    if starting_key:
        found = False
        for key, value in metadata.items():
            if key == starting_key:
                found = True
            elif found:
                print('INIT PAPER:', metadata[key]['title'])
                if metadata[key]['title']:
                    with open(cache_path, 'a') as f:
                        f.write(metadata[key]['title'] + '\n')
                        
                    titles = get_references(metadata[key])
                    print('references found')
                    ids = find_papers(titles, headers)
                    print('IDS:', ids)
                    get_papers_batch(ids)
                    print('SLEEPING ZZzzz...')
                    sleep(30)
