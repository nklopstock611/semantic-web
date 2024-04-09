import os
import json
import scipdf
import xml_analyzer as xmlq
import extractor as extr

# def main():
#     i = 1
#     with open('/home/estudiante/semantic-web/first-task/pdf-downloader/publication_dates_2.json', 'r', encoding='utf-8') as f:
#         json_dict = json.load(f)
#         for each_paper in json_dict:
#             pdf_file = json_dict[each_paper][3]
#             if pdf_file[-4::] == '.pdf':
#                 try:
# 		              pdf_path = "/home/estudiante/semantic-web/first-task/pdf-downloader/pdfs/" + pdf_file
#                     print('Extracting Metadata From', json_dict[each_paper][3])
#                     with open(pdf_path, 'r', encoding='utf-8') as pdf:
#                         article = scipdf.parse_pdf(pdf_path, soup=True)
#                         metadata = xmlq.xml_query(article)
#                         # extr.create_csv(metadata)
#                         extr.create_json(metadata)
#                         print(i)
#                         i += 1
#                     except AttributeError:
#                         print('Error while parsing PDF to XML')
# 		    except FileNotFoundError:
#                          print('PDF not found!')

def make_pdfs_set(json_dict: dict):
    pdfs = set()
    for each_paper in json_dict:
        pdf_file = json_dict[each_paper][3]
        if pdf_file[-4::] == '.pdf':
            pdfs.add(pdf_file[:-4])

    return pdfs

def main():
    pdfs_dir = '/workspaces/semantic-web/first-task/pdf-downloader/pdfs/'
    with open('/workspaces/semantic-web/first-task/pdf-downloader/publication_dates_2.json', 'r', encoding='utf-8') as f:
        json_dict = json.load(f)

    pdfs = make_pdfs_set(json_dict)
    for each_pdf in os.listdir(pdfs_dir):
        if each_pdf.endswith('.pdf'):
            pdf_name = each_pdf[:-4]
            in_json = pdf_name in pdfs
            try:
		        # pdf_path = "/home/estudiante/semantic-web/first-task/pdf-downloader/pdfs/" + pdf_file
                pdf_path = pdfs_dir + each_pdf
                print('Extracting Metadata From', pdf_name)
                article = scipdf.parse_pdf(pdf_path, soup=True)
                metadata = xmlq.xml_query(article, in_json)
                # extr.create_csv(metadata)
                extr.create_json(metadata)
                print(i)
                i += 1
            except AttributeError:
                print('Error while parsing PDF to XML')
            except FileNotFoundError:
                print('PDF not found!')



if __name__ == '__main__':
    main()
