"""
Entrega 1 - Proyecto Semantic Web

Integrantes:
- Alejandro Salgado
- Miguel Zapata
- Nicolás Klopstock
"""
import json
import logic as l

def main():
    with open('./dict_split_2_1.json') as f:
        papers = json.load(f)

    for each_paper in papers:
        # data[papers[each_paper]['title']] = papers[each_paper]['year']

        # print(l.get_pdf_link(papers[each_paper]))
        print(l.download_pdf(papers[each_paper]))

if __name__ == '__main__':
    main()
