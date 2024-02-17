from bs4 import BeautifulSoup

with open('C:/Users/nklop/Universidad/Séptimo Semestre/Semantic Web/semantic-web/firstTask/xml-analyzer/xmls/SSDBM09_PTS.pdf.tei.xml', 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'lxml')

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
"""

idno = soup.find('idno').text
metadata[idno] = {}

metadata_indv = {}
title = soup.find('title').text
metadata[idno]['title'] = title

metadata[idno]['authors'] = []
for each_author in soup.find_all('author'):
    metadata_author = {}
    metadata_author['forename'] = each_author.find('forename').text
    metadata_author['surname'] = each_author.find('surname').text
    metadata_author['email'] = each_author.find('email').text

    affiliation = soup.find('affiliation')
    metadata_author['affiliation'] = affiliation.find('orgname', type="institution").text
    metadata_author['addressLine'] = affiliation.find('addrline').text
    metadata_author['postCode'] = affiliation.find('postcode').text
    metadata_author['settlement'] = affiliation.find('settlement').text
    metadata_author['country'] = affiliation.find('country').text

    metadata[idno]['authors'].append(metadata_author)

# metadata[idno]['year'] = soup.find('publicationstmt').find('date').text
metadata[idno]['abstract'] = soup.find('abstract').text

print(metadata)




