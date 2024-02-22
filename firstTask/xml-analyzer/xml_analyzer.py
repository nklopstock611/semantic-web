import json
from bs4 import BeautifulSoup

metadata = {}
"""
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
        'note': '<note>'
}
"""

# ======================= #
# QUERIES FOR HEADER FILE #
# ======================= #

with open('C:/Users/nklop/Universidad/Séptimo Semestre/Semantic Web/semantic-web/firstTask/xml-analyzer/xmls/SSDBM09_PTS.pdf.tei.xml', 'r', encoding='utf-8') as f:
    content = f.read()

soup_header = BeautifulSoup(content, 'lxml')

idno = soup_header.find('idno').text
metadata[idno] = {}

metadata_indv = {}
title = soup_header.find('title').text
metadata[idno]['title'] = title

metadata[idno]['authors'] = []
for each_author in soup_header.find_all('author'):
    metadata_author = {}
    metadata_author['forename'] = each_author.find('forename').text
    metadata_author['surname'] = each_author.find('surname').text
    metadata_author['email'] = each_author.find('email').text

    affiliation = soup_header.find('affiliation')
    metadata_author['affiliation'] = affiliation.find('orgname', type="institution").text
    metadata_author['addressLine'] = affiliation.find('addrline').text
    metadata_author['postCode'] = affiliation.find('postcode').text
    metadata_author['settlement'] = affiliation.find('settlement').text
    metadata_author['country'] = affiliation.find('country').text

    metadata[idno]['authors'].append(metadata_author)

with open('C:/Users/nklop/Universidad/Séptimo Semestre/Semantic Web/semantic-web/firstTask/pdf-downloader/publication_dates.json', 'r') as f:
    obj = json.load(f)
    metadata[idno]['year'] = obj[title][0]

metadata[idno]['abstract'] = soup_header.find('abstract').text

# =========================== #
# QUERIES FOR REFERENCES FILE #
# =========================== #

with open('C:/Users/nklop/Universidad/Séptimo Semestre/Semantic Web/semantic-web/firstTask/xml-analyzer/xmls/SSDBM09_PTS-References.pdf.tei.xml', 'r', encoding='utf-8') as f:
    content = f.read()

soup_references = BeautifulSoup(content, 'lxml')

metadata[idno]['references'] = []
for each_reference in soup_references.find_all('biblstruct'):
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
    metadata_references['year'] = each_reference.find('date').text
    metadata_references['note'] = each_reference.find('note').text if each_reference.find('note') else None

    metadata[idno]['references'].append(metadata_references)

print(metadata)




