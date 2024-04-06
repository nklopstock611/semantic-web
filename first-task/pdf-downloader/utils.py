import json
import requests
from time import sleep

with open('./credentials.json') as f:
    json_obj = json.load(f)

api_key = json_obj["API_KEY_SS"]

headers = {
    'x-api-key': api_key,
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

with open('C:/Users/nklop/Universidad/Septimo Semestre/Semantic Web/semantic-web/first-task/metadata.json') as f:
    metadata = json.load(f)
    
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

def get_references(metadata) -> list:
    titles = []
    for each_paper in metadata:
        references = metadata[each_paper]['references']
        for each_reference in references:
            titles.append(each_reference['title'])
    return titles

def find_papers(papers_titles: list) -> dict:
    ids = []
    for each_paper in papers_titles:
        query_params = {'query': each_paper,
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
                ids.append(ret['data'][0]['paperId'])
                print('FOUND:', ret['data'][0]['title'])
                sleep(2)
            except KeyError:
                print('Error: No "data" key')
        else:
            print(f"Error: {response.status_code}")
            print(json.dumps(response.json(), indent=2))
    
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
        print(f"Paper: {ret['title']}")
        print(f"PDF: {ret['isOpenAccess']}")
        if ret['isOpenAccess'] and ret['openAccessPdf']:
            if ret['openAccessPdf']['url'][:-4] == '.pdf':
                download_paper(ret)
        return ret
    else:
        print(f"Error: {response.status_code}")
        print(json.dumps(response.json(), indent=2))

def download_paper(paper: dict):
    """
    Downloads the paper from the url.
    """
    url = paper['openAccessPdf']['url']
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"C:/Users/nklop/Universidad/Septimo Semestre/Semantic Web/semantic-web/first-task/pdf-downloader/spdfs/{paper['paperId']}.pdf", 'wb') as f:
            f.write(response.content)
    else:
        print(f"Error: {response.status_code}")
        print(json.dumps(response.json(), indent=2))

if __name__ == '__main__':
    titles = get_references(metadata)
    print('references found')
    ids = find_papers(titles)
    print('IDS:', ids)
    get_papers_batch(ids)
    # download_paper(get_papers_batch(ids))