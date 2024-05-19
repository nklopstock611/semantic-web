import shapes as shs

import logging
from typing import List
from neo4j import GraphDatabase

url = "bolt://localhost:7687/neo4j"
username = "neo4j"
password = "neo4j"

neo4j_driver = GraphDatabase.driver(url, auth=(username, password))

def get_db():
    try:
        return neo4j_driver.session()
    except Exception as e:
        print("Error connecting to Neo4j:", e)
        raise

def get_authors_from_paper(paper: str) -> List[str]:
    """
    Query that gets authors from a paper.
    """
    db = get_db()
    query = 'MATCH (a:ns0__Author)-[:ns0__isAuthorOf]->({uri: $paper_uri}) RETURN a.ns0__Forename + " " + a.ns0__Surname as authors'
    nodes = []
    try:
        with db as session:
            result = session.run(query, paper_uri=f"http://www.uniandes.web.semantica.example.org/{paper}")
            for record in result:
                nodes.append(record['authors'])
    finally:
        db.close()
        
    return nodes

def get_pdfs_from_keyword(keyword: str, limit: str='10') -> List[str]:
    """
    Query that gets papers related to a keyword.
    """
    db = get_db()
    query = 'MATCH (p:ns0__Paper)-[:ns0__hasConcept_Annotation]->(c:ns0__ConceptAnnotation {uri: $keyword_uri}) RETURN p.uri as pUri LIMIT ' + limit
    nodes = []
    try:
        with db as session:
            result = session.run(query, keyword_uri=f"http://www.uniandes.web.semantica.example.org/{keyword}", limit=limit)
            for record in result:
                nodes.append(record['pUri'].replace('http://www.uniandes.web.semantica.example.org/', ''))
    finally:
        db.close()

    return nodes

def get_recommendation_for_given_paper(paper: str) -> List[str]:
    """
    Query that gets recommendations for a given paper.
    """
    query = """
    MATCH (p:ns0__Paper {uri: $paper_uri})-[:ns0__hasConcept_Annotation]->(k:ns0__ConceptAnnotation)
    WITH p, collect(k) AS keywords

    MATCH (k:ns0__ConceptAnnotation)<-[:ns0__hasConcept_Annotation]-(otherPaper:ns0__Paper)
    WHERE k IN keywords AND otherPaper <> p

    WITH otherPaper, collect(k.uri) as sharedKeywordsName, COUNT(k) AS sharedKeywords
    ORDER BY sharedKeywords DESC

    RETURN otherPaper.ns0__Title AS paper, sharedKeywords, sharedKeywordsName LIMIT 10
    """
    db = get_db()
    nodes = []
    try:
        with db as session:
            result = session.run(query, paper_uri=f"http://www.uniandes.web.semantica.example.org/{paper}")
            for record in result:
                nodes.append({
                    'paper': record['paper'].replace('_', ' '),
                    'sharedKeywordsCount': record['sharedKeywords'],
                    'sharedKeywordNames': [
                        keyword.replace('http://www.uniandes.web.semantica.example.org/', '').replace('_', ' ')
                        for keyword in record['sharedKeywordsName']
                    ]
                })
    finally:
        db.close()

    return nodes

def get_papers_by_author(author: str) -> List[str]:
    """
    Query that gets papers by author.
    """
    query = """
    MATCH (a:ns0__Author {uri: $author_uri})-[:ns0__isAuthorOf]->(p)
    WHERE p:ns0__Paper OR p:ns0__Reference
    RETURN p.ns0__Title AS paper, p.ns0__Paper_pdf as pdf
    """
    db = get_db()
    nodes = []
    try:
        with db as session:
            result = session.run(query, author_uri=f"http://www.uniandes.web.semantica.example.org/{author}")
            for record in result:
                nodes.append({
                    'title': record['paper'].replace('_', ' '),
                    'downloaded_pdf': record['pdf']
                })
    finally:
        db.close()

    return nodes

def load_rdf_to_neo4j(rdf_data, rdf_format='RDF/XML'):
    """
    Función para cargar RDF en Neo4j usando neosemantics mediante la librería neo4j.
    """
    db = get_db()
    serialized = rdf_data.serialize(format='xml')
    print('SERIALIZED:', serialized)
    cypher_query = """
    CALL n10s.rdf.import.inline($rdf_data, $rdf_format)
    """
    with db as session:
        session.run(cypher_query, rdf_data=serialized, rdf_format=rdf_format)

def insert_triple(data: dict) -> bool:
    try:
        data_graph = shs.create_graph(data)
        
        if shs.validate_shape(data_graph):
            load_rdf_to_neo4j(data_graph)
            return True
        else:
            logging.error("Validation failed for the provided data.")
            return False
    except Exception as e:
        logging.error(f"An error occurred while inserting triple: {e}")
        return False
