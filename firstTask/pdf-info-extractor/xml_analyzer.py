import json
from bs4 import BeautifulSoup

def get_meeting_address(string: str) -> tuple:
    """
    Seperates the meeting and address from the string.
    """
    meeting = None
    address = None
    index_address = None
    
    index_comma = string.rfind(',')
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
            'year': '<year>',
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
            'year': '<year>',
            'meeting': '<meeting>',
            'place': '<place>',
            'note': '<note>'
    }
    """
    metadata = {}

    idno = soup_obj.find('idno').text
    metadata[idno] = {}

    title = soup_obj.find('title').text
    metadata[idno]['title'] = title

    metadata[idno]['authors'] = []
    for each_author in soup_obj.find('analytic').find_all('author'):
        metadata_author = {}
        metadata_author['forename'] = each_author.find('forename').text
        metadata_author['surname'] = each_author.find('surname').text
        metadata_author['email'] = each_author.find('email').text

        affiliation = soup_obj.find('affiliation')
        metadata_author['affiliation'] = affiliation.find('orgname', type="institution").text
        metadata_author['addressLine'] = affiliation.find('addrline').text
        metadata_author['postCode'] = affiliation.find('postcode').text
        metadata_author['settlement'] = affiliation.find('settlement').text
        metadata_author['country'] = affiliation.find('country').text

        metadata[idno]['authors'].append(metadata_author)

    with open('C:/Users/nklop/Universidad/Séptimo Semestre/Semantic Web/semantic-web/firstTask/pdf-downloader/publication_dates.json', 'r') as f:
        obj = json.load(f)
        metadata[idno]['year'] = obj[title][0]

    metadata[idno]['abstract'] = soup_obj.find('abstract').text

    metadata[idno]['references'] = []
    for each_reference in soup_obj.find_all('biblstruct'):
        metadata_references = {}
        metadata_references = {}
        metadata_references['title'] = each_reference.find('title').text
        references_authors = []
        for each_author in each_reference.find_all('author'):
            metadata_author = {}
            metadata_author['forename'] = each_author.find('forename').text
            metadata_author['surname'] = each_author.find('surname').text
            references_authors.append(metadata_author)
        metadata_references['authors'] = references_authors
        metadata_references['publication_date'] = each_reference.find('date').text
        meeting, address = get_meeting_address(each_reference.find('meeting').text if each_reference.find('meeting') else 'None')
        metadata_references['meeting'] = meeting
        metadata_references['place'] = address
        metadata_references['note'] = each_reference.find('note').text if each_reference.find('note') else None

        metadata[idno]['references'].append(metadata_references)

    return metadata
