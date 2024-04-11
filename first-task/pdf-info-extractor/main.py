import os
import json
import scipdf
import xml_analyzer as xmlq
import extractor as extr

pdfs_path = '/semantic-web/first-task/pdf-downloader/pdfs/'
seen_pdfs_path = '/semantic-web/first-task/pdf-downloader/publication_dates_2.json'

def make_pdfs_set(json_dict: dict):
    """
    Makes a set of PDFs from the JSON dictionary.
    """
    pdfs = set()
    for each_paper in json_dict:
        pdf_file = json_dict[each_paper][3]
        if pdf_file[-4::] == '.pdf':
            pdfs.add(pdf_file[:-4])

    return pdfs

def main():
    with open(seen_pdfs_path, 'r', encoding='utf-8') as f:
        json_dict = json.load(f)

    pdfs = make_pdfs_set(json_dict)
    print('PDFs EN JSON', len(pdfs))
    i = 1
    for each_pdf in os.listdir(pdfs_path):
        if each_pdf.endswith('.pdf'):
            pdf_name = each_pdf[:-4]
            in_json = pdf_name in pdfs
            try:
                pdf_path = pdfs_path + each_pdf
                print('Extracting Metadata From', pdf_path, in_json)
                with open(pdf_path, 'r', encoding='utf-8') as pdf:
                    article = scipdf.parse_pdf(pdf_path, soup=True)
                    print('Got Article!')
                    metadata = xmlq.xml_query(article, each_pdf, in_json)
                    print('Got Metadata!')
                    # extr.create_csv(metadata)
                    extr.create_json(metadata)
                    print('JSON Modified!')
                    print(i)
                    i += 1
            except AttributeError:
                print('Error while parsing PDF to XML')
            except FileNotFoundError:
                print('PDF not found!')

if __name__ == '__main__':
    main()
