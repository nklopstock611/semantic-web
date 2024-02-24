import json
from bs4 import BeautifulSoup

def get_meeting_address(string: str) -> tuple:
    """
    Seperates the meeting and address from the string.
    """
    meeting = ''
    address = ''
    index_address = None
    
    index_comma = string.rfind(',')
    if index_comma == -1:
        return (string, '')
    
    for i in range(index_comma - 1, -1, -1):
        if string[i].isupper():
            index_address = i
            break
        
    if index_address != None:
        meeting = string[:index_address]
        address = string[index_address:]
    
    return (meeting, address)

def xml_query(soup_obj: BeautifulSoup):
    """
    This function receives a BeautifulSoup object and returns a dictionary with the metadata of the article.

    {
        '<IDNO>': {
            'title': '<title>',
            'authors': ['<author>', '<author>', ...],
            'publication_year': '<year>',
            'abstract': '<abstract>',
            'references': ['<reference>', '<reference>', ...]
        },
    }

    {
        '<author_name>': {
            'forename': '<author_name>',
            'surname': '<author_name>',
            'email': '<email>',
            'affiliation': '<affiliation>',
            'addressLine': '<address>',
            'postCode': '<postCode>',
            'settlement': '<settlement>',
            'country': '<country>'
        }
    }

    {
        '<reference>': {
            'title': '<title>',
            'authors': ['<author>', '<author>', ...],
            'publication_year': '<year>',
            'meeting': '<meeting>',
            'city': '<city>',
            'country': '<country>',
            'note': '<note>'
    }
    """
    metadata = {}

    idno = soup_obj.find('idno').text
    metadata[idno] = {}

    title = soup_obj.find('title').text
    metadata[idno]['title'] = title.replace(';', ',')

    metadata[idno]['authors'] = []
    for each_author in soup_obj.find('analytic').find_all('author'):
        metadata_author = {}
        metadata_author['forename'] = each_author.find('forename').text if each_author.find('forename') else ''
        metadata_author['surname'] = each_author.find('surname').text if each_author.find('surname') else ''
        metadata_author['email'] = each_author.find('email').text if each_author.find('email') else ''

        affiliation = soup_obj.find('affiliation')
        metadata_author['affiliation'] = (affiliation.find('orgname', type="institution").text).replace(';', ',') if affiliation.find('orgname', type="institution") else ''
        metadata_author['addressLine'] = (affiliation.find('addrline').text).replace(';', ',') if affiliation.find('addrline') else ''
        metadata_author['postCode'] = (affiliation.find('postcode').text).replace(';', ',') if affiliation.find('postcode') else ''
        metadata_author['settlement'] = (affiliation.find('settlement').text).replace(';', ',') if affiliation.find('settlement') else ''
        metadata_author['country'] = (affiliation.find('country').text).replace(';', ',') if affiliation.find('country') else ''

        metadata[idno]['authors'].append(metadata_author)

    with open('C:/Users/nklop/Universidad/Séptimo Semestre/Semantic Web/semantic-web/firstTask/pdf-downloader/publication_dates.json', 'r') as f:
        obj = json.load(f)
        metadata[idno]['publication_year'] = obj[title][0]

    metadata[idno]['abstract'] = ((soup_obj.find('abstract').text).replace(';', '')).replace('\n', '') if soup_obj.find('abstract') else ''

    metadata[idno]['references'] = []
    for each_reference in soup_obj.find_all('biblstruct'):
        metadata_references = {}
        metadata_references = {}
        metadata_references['title'] = (each_reference.find('title').text).replace(';', ',') if each_reference.find('title') else ''
        references_authors = []
        for each_author in each_reference.find_all('author'):
            metadata_author = {}
            metadata_author['forename'] = (each_author.find('forename').text).replace(';', ',') if each_author.find('forename') else ''
            metadata_author['surname'] = (each_author.find('surname').text).replace(';', ',') if each_author.find('surname') else ''
            references_authors.append(metadata_author)
        metadata_references['authors'] = references_authors
        metadata_references['publication_date'] = (each_reference.find('date').text).replace(';', ',') if each_reference.find('date') else ''
        meeting, address = get_meeting_address(each_reference.find('meeting').text if each_reference.find('meeting') else '')
        metadata_references['meeting'] = meeting.replace(';', ',')
        metadata_references['city'] = (address.split(',')[0] if address else '').replace(';', ',')
        metadata_references['country'] = (address.split(',')[1] if address else '').replace('.', '')
        metadata_references['note'] = (each_reference.find('note').text).replace(';', ',') if each_reference.find('note') else ''

        metadata[idno]['references'].append(metadata_references)

    return metadata
