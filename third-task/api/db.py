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

def get_pdfs_from_keyword(keyword: str, limit: str ='10') -> List[str]:
    db = get_db()
    query = 'MATCH (p:ns0__Paper)-[:ns0__hasConcept_Annotation]->(c:ns0__ConceptAnnotation {uri: "http://www.uniandes.web.semantica.example.org/' + keyword + '"}) RETURN p.uri as pUri LIMIT ' + limit
    nodes = []
    try:
        with db as session:
            result = session.run(query, keyword_uri=f"http://www.uniandes.web.semantica.example.org/{keyword}", limit=limit)
            for record in result:
                nodes.append(record['pUri'].replace('http://www.uniandes.web.semantica.example.org/', ''))
    finally:
        db.close()

    return nodes
