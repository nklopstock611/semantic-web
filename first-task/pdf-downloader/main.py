"""
Entrega 1 - Proyecto Semantic Web
8 marzo 2024

Integrantes:
- Alejandro Salgado
- Miguel Zapata
- Nicolás Klopstock
"""
import json
import logic as l
import requester as r

def main():
    with open('./dict_split_2.json') as f:
        papers = json.load(f)

    items = list(papers.items())
    starting_key = next((clave for clave, valor in papers.items() if valor['title'] == "A study of information seeking and retrieving, iii: Searchers, searces, overlap"), None)

    i = 1
    print(len(papers))
    if starting_key:
        found = False
        for key, value in papers.items():
            i += 1
            if key == starting_key:
                found = True
                print(i)
            if found:
                print(f"Paper: {papers[key]['title']}")
                print(l.download_pdf(papers[key]))

if __name__ == '__main__':
   main()
