"""
Entrega 1 - Proyecto Semantic Web

Integrantes:
- Alejandro Salgado
- Miguel Zapata
- Nicolás Klopstock
"""
import json
import logic as l

def create_publication_dates_json():
    try:
        with open('C:/Users/nklop/Universidad/Séptimo Semestre/Semantic Web/semantic-web/firstTask/pdf-downloader/publication_dates.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data_in_json(data: dict):
    with open('C:/Users/nklop/Universidad/Séptimo Semestre/Semantic Web/semantic-web/firstTask/pdf-downloader/publication_dates.json', 'w') as f:
        json.dump(data, f, indent=4)

def main():
    with open('./dict_split_2.json') as f:
        papers = json.load(f)

    for each_paper in papers:
        data = create_publication_dates_json()
        data[papers[each_paper]['title']] = papers[each_paper]['year']
        save_data_in_json(data)

        # print(l.get_pdf_link(papers[each_paper]))
        print(l.download_pdf(papers[each_paper]))

if __name__ == '__main__':
    main()
