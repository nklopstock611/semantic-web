import re
import json
import random
from bs4 import BeautifulSoup

pattern = re.compile(r'\[.*?\]')
seen_pdfs_path = '/home/estudiante/semantic-web/first-task/pdf-downloader/publication_dates_2.json'

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

def xml_query(soup_obj: BeautifulSoup, is_in_json: bool):
    """
    This function receives a BeautifulSoup object and returns a dictionary with the metadata of the article.

    {
        '<IDNO>': {
            'title': '<title>',
            'authors': ['<author>', '<author>', ...],
            'publication_year': '<year>',
            'introduction': '<introduction>',
            'abstract': '<abstract>',
            'conclusions': '<conclusions>',
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

    idno = soup_obj.find('idno').text if soup_obj.find('idno') != '' else random.randint(0, 150000)
    print(idno)
    metadata[idno] = {}

    title = soup_obj.find('title').text if soup_obj.find('title') else None

    if title:
        metadata[idno]["paper_title"] = title.replace(';', ',')
    else:
        metadata[idno]["paper_title"] = None

    metadata[idno]["paper_authors"] = []
    for each_author in soup_obj.find('analytic').find_all('author'):
        metadata_author = {}
        metadata_author["paper_author_forename"] = each_author.find('forename').text if each_author.find('forename') else ''
        metadata_author["paper_author_surname"] = each_author.find('surname').text if each_author.find('surname') else ''
        metadata_author["paper_author_email"] = each_author.find('email').text if each_author.find('email') else ''

        affiliation = soup_obj.find('affiliation')
        metadata_author["paper_author_affiliation"] = (affiliation.find('orgname', type="institution").text).replace(';', ',') if affiliation.find('orgname', type="institution") else ''
        metadata_author["paper_author_address_line"] = (affiliation.find('addrline').text).replace(';', ',') if affiliation.find('addrline') else ''
        metadata_author["paper_author_post_code"] = (affiliation.find('postcode').text).replace(';', ',') if affiliation.find('postcode') else ''
        metadata_author["paper_author_settlement"] = (affiliation.find('settlement').text).replace(';', ',') if affiliation.find('settlement') else ''
        metadata_author["paper_author_country"] = (affiliation.find('country').text).replace(';', ',') if affiliation.find('country') else ''

        metadata[idno]["paper_authors"].append(metadata_author)

    if is_in_json:
        with open(seen_pdfs_path, 'r') as f:
            obj = json.load(f)
            print(title)
            metadata[idno]["paper_publication_year"] = obj[title][0] if title in obj else None

    divs = soup_obj.find_all('div', attrs={'xmlns': 'http://www.tei-c.org/ns/1.0'})
    filtered_divs = [div for div in divs if "Introduction" in div.text]
    introduction = [re.sub(pattern, '', e.find('p').text) for e in filtered_divs if e.find('p')]
    if introduction:
        metadata[idno]["paper_introduction"] = introduction[0]
    metadata[idno]["paper_abstract"] = ((soup_obj.find('abstract').text).replace(';', '')).replace('\n', '') if soup_obj.find('abstract') else ''
    filtered_divs = [div for div in divs if "Conclusions" in div.text]
    conclusion = [re.sub(pattern, '', e.find('p').text) for e in filtered_divs if e.find('p')]
    if conclusion:
        metadata[idno]["paper_conclusions"] = conclusion[0]

    metadata[idno]["paper_references"] = []
    for each_reference in soup_obj.find_all('biblstruct'):
        metadata_references = {}
        metadata_references = {}
        metadata_references["reference_paper_title"] = (each_reference.find('title').text).replace(';', ',') if each_reference.find('title') else ''
        references_authors = []
        for each_author in each_reference.find_all('author'):
            metadata_author = {}
            metadata_author["reference_paper_author_forename"] = (each_author.find('forename').text).replace(';', ',') if each_author.find('forename') else ''
            metadata_author["reference_paper_author_surname"] = (each_author.find('surname').text).replace(';', ',') if each_author.find('surname') else ''
            references_authors.append(metadata_author)
        metadata_references["reference_paper_authors"] = references_authors
        metadata_references["reference_paper_publication_date"] = (each_reference.find('date').text).replace(';', ',') if each_reference.find('date') else ''
        meeting, address = get_meeting_address(each_reference.find('meeting').text if each_reference.find('meeting') else '')
        metadata_references["reference_paper_meeting"] = meeting.replace(';', ',')
        metadata_references["reference_paper_city"] = (address.split(',')[0] if address else '').replace(';', ',')
        metadata_references["reference_paper_country"] = (address.split(',')[1] if address else '').replace('.', '')
        metadata_references["reference_paper_note"] = (each_reference.find('note').text).replace(';', ',') if each_reference.find('note') else ''

        metadata[idno]["paper_references"].append(metadata_references)

    return metadata
