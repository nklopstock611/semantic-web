from neo4j import GraphDatabase

url = "bolt://localhost:7687"
username = "neo4j"
password = "neo4j"

neo4j_driver = GraphDatabase.driver(url, auth=(username, password))

def get_db():
    try:
        return neo4j_driver.session()
    except Exception as e:
        print("Error connecting to Neo4j:", e)
        raise

def get_pdfs_from_keyword(keyword: str, limit: str ='10'):
    db = get_db()
    query = 'MATCH (p:ns0__Paper)-[:ns0__hasConcept_Annotation]->(c:ns0__ConceptAnnotation {uri: "http://www.uniandes.web.semantica.example.org/' + keyword + '}) RETURN p.uri as pUri LIMIT' + limit
    nodes = []
    with db as session:
        result = session.run(query)
        for record in result:
            nodes.append(record['pUri'])

    return jsonify(nodes)
