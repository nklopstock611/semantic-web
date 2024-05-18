import re
import os
import uuid
import scipdf
import random
from bs4 import BeautifulSoup

pattern = re.compile(r'\[.*?\]')

def sanitize_filename(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in (' ', '.', '_', '-')]).rstrip()

async def parse_pdf(file):
    """
    Parses a PDF file and returns the XML representation.
    """
    # temp_filename = f"{uuid.uuid4()}.pdf"
    original_filename = sanitize_filename(file.filename)
    temp_filepath = f"./temp_files/{original_filename}"

    # Crear directorio temporal si no existe
    os.makedirs(os.path.dirname(temp_filepath), exist_ok=True)
    with open(temp_filepath, "wb") as buffer:
        buffer.write(await file.read())
    
    xml = scipdf.parse_pdf(temp_filepath, soup=True)

    # os.remove(temp_filepath) # ¿? ¿? ¿? ¿? ¿será?

    return xml

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

def xml_query(soup_obj: BeautifulSoup, pdf_name: str):
    """
    Returns a dictionary with the metadata of the article.
    soup_obj: Article in XML format.
    """
    metadata = {}
    
    idno = idno = soup_obj.find('idno').text if soup_obj.find('idno') != '' else random.randint(0, 150000)
    metadata[idno] = {}
    
    metadata[idno]["paper_downloaded_pdf"] = pdf_name
    
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
        
    metadata[idno]["paper_publication_date"] = (soup_obj.find('date').text).replace(';', ',') if soup_obj.find('date') else ''

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