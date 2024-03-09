import json

import scipdf
import xml_analyzer as xmlq

def verify_unique_papers(file_path: str='/home/estudiante/semantic-web/firstTask/pdf-downloader/publication_dates_2.json'):
    """
    Verifies if all the papers are unique in the saved dataset.
    """
    with open(file_path, 'r') as f:
       json_dict = json.load(f)
       papers_seen = {}
       print(len(json_dict))
       json_dict_min = {k.lower(): v for k, v in json_dict.items()}
       for each_paper in json_dict_min:
           if each_paper.lower() in papers_seen:
               del each_paper
           else:
               papers_seen[each_paper] = None

       print(len(papers_seen))

       with open(file_path, 'w') as f:
           json.dump(json_dict, f)

    return None

def create_csv(metadata: dict) -> None:
    with open('metadata.csv', 'w', encoding='utf-8') as file:
        file.write('idno;title;publication_year;abstract;authorForename;authorSurname;authorEmail;authorAffiliation;authorAddressLine;authorPostCode;authorS>
        for each_article in metadata:
            file.write(each_article + ';' + metadata[each_article]['title'] + ';' + metadata[each_article]['publication_year'] + ';' + metadata[each_article>
            for i, author in enumerate(metadata[each_article]['authors']):
                if i == 0:
                    file.write(author['forename'] + ';' + author['surname'] + ';' + author['email'] + ';' + author['affiliation'] + ';' + author['addressLin>
                else:
                    file.write(';;;;' + author['forename'] + ';' + author['surname'] + ';' + author['email'] + ';' + author['affiliation'] + ';' + author['a>
            for i, reference in enumerate(metadata[each_article]['references']):
                file.write(';;;;;;;;;;;;' + reference['title'] + ';' + reference['publication_date'] + ';' + reference['meeting'] + ';' + reference['city'] >
                for i, author in enumerate(reference['authors']):
                    if i == 0:
                        file.write(';' + author['forename'] + ';' + author['surname'] + '\n')
                    else:
                        file.write(';;;;;;;;;;;;;;;;;;' + author['forename'] + ';' + author['surname'] + '\n')

def create_json(metadata: dict) -> None:
    for each_article in metadata:
        with open('metadata.json', 'r') as f:
            json_dict = json.load(f)

        json_dict.update({ each_article: metadata[each_article] })

        with open('metadata.json', 'w') as f:
            json.dump(json_dict, f)
