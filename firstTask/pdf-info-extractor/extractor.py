import xml_analyzer as xmlq
import scipdf

article = scipdf.parse_pdf('C:/Users/nklop/Universidad/Séptimo Semestre/Semantic Web/semantic-web/firstTask/pdf-downloader/pdfs/SSDBM09_PTS.pdf', soup=True)
metadata = xmlq.xml_query(article)

def create_csv(metadata: dict) -> None:
    with open('metadata.csv', 'w', encoding='utf-8') as file:
        file.write('idno;title;publication_year;abstract;authorForename;authorSurname;authorEmail;authorAffiliation;authorAddressLine;authorPostCode;authorSettlement;authorCountry;referenceTitle;referencePublicationDate;referenceMeeting;referenceCity;referenceCountry;referenceNote;referenceAuthorForename;referenceAuthorSurname\n')
        for each_article in metadata:    
            file.write(each_article + ';' + metadata[each_article]['title'] + ';' + metadata[each_article]['publication_year'] + ';' + metadata[each_article]['abstract'] + ';')
            for i, author in enumerate(metadata[each_article]['authors']):
                if i == 0:
                    file.write(author['forename'] + ';' + author['surname'] + ';' + author['email'] + ';' + author['affiliation'] + ';' + author['addressLine'] + ';' + author['postCode'] + ';' + author['settlement'] + ';' + author['country'] + '\n')
                else:
                    file.write(';;;;' + author['forename'] + ';' + author['surname'] + ';' + author['email'] + ';' + author['affiliation'] + ';' + author['addressLine'] + ';' + author['postCode'] + ';' + author['settlement'] + ';' + author['country'] + '\n')
            for i, reference in enumerate(metadata[each_article]['references']):
                file.write(';;;;;;;;;;;;' + reference['title'] + ';' + reference['publication_date'] + ';' + reference['meeting'] + ';' + reference['city'] + ';' + reference['country'] + ';' + reference['note'])
                for i, author in enumerate(reference['authors']):
                    if i == 0:
                        file.write(';' + author['forename'] + ';' + author['surname'] + '\n')
                    else:
                        file.write(';;;;;;;;;;;;;;;;;;' + author['forename'] + ';' + author['surname'] + '\n')
            
create_csv(metadata)
