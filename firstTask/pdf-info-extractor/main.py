import json
import scipdf
import xml_analyzer as xmlq
import extractor as extr

def main():
    i = 1
    with open('/home/estudiante/semantic-web/firstTask/pdf-downloader/publication_dates_2.json', 'r', encoding='utf-8') as f:
        json_dict = json.load(f)
        for each_paper in json_dict:
            pdf_file = json_dict[each_paper][3]
            if pdf_file[-4::] == '.pdf':
                pdf_path = "/home/estudiante/semantic-web/firstTask/pdf-downloader/spdfs/" + pdf_file
                print('Extracting Metadata From', json_dict[each_paper][3])
                with open(pdf_path, 'r', encoding='utf-8') as pdf:
                    try:
                       article = scipdf.parse_pdf(pdf_path, soup=True)
                       metadata = xmlq.xml_query(article)
                       # extr.create_csv(metadata)
                       extr.create_json(metadata)
                       print(i)
                       i += 1
                    except AttributeError:
                       print('Error while parsing PDF to XML')

if __name__ == '__main__':
    main()
