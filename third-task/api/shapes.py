import json
from datetime import datetime
from rdflib import Graph, Literal, RDF, URIRef, Namespace, BNode, XSD, Bag, Seq
from rdflib.namespace import RDF, RDFS, OWL
from pyshacl import validate

shapes_path = './shapes/shapes.ttl'

def get_shape_graph(shapes_path):
    shape_graph = Graph()
    try:
        shape_graph.parse(shapes_path, format='ttl')
        print("Shapes loaded successfully.")
    except Exception as e:
        print("Failed to load shapes:", e)
    return shape_graph

SHAPE_GRAPH = get_shape_graph(shapes_path)

def instance_exists(graph, instance_uri):
    """
    Verificar si una instancia ya existe en la ontología
    """
    return (instance_uri, None, None) in graph

def group_keywords(given_keywords: str) -> dict:
    """
    Formats the given keywords from the user's input.
    Example: "algorithm, timing analysis" -> {"entities": ['algorithm', 'timing analysis']}
    """
    keywords = {}
    keywords['entities'] = given_keywords.split(',')
    return keywords

def format_date(given_date: str):
    return datetime.strptime(given_date, "%Y-%m-%d").date()

def create_graph(datos: dict):
    g = Graph()

    g.bind('rdf', RDF)
    g.bind('rdfs', RDFS)
    g.bind('owl', OWL)
    g.bind("xsd", XSD)

    UEX = Namespace("http://www.uniandes.web.semantica.example.org/")
    UEV = Namespace("http://www.uniandes.web.semantica.ejemplo.org/voca#")
    g.bind('uex', UEX)
    g.bind('uev', UEV)
    
    # Iteramos sobre cada paper usando su ID único
    for paper_id, paper_content in datos.items():
        # print('DATA:', paper_content)
        # El titulo es lo que se carga como clase en la ontología
        paper_class = paper_content.get('paper_title', '').lower().replace(' ', '_') # Crear un URI para el paper usando el ID del paper
        # print('TITLE:', paper_class)
        if paper_class != '' and paper_class is not None:
            # pasar a minúsculas y reemplazar espacios por guiones bajos
            paper_class = paper_class.lower().replace(' ', '_')
            # Elimina caracteres ?,\," y ' de la clase
            paper_class = paper_class.replace('?', '').replace(',', '').replace('"', '').replace("'", '')
            paper_uri = UEX[paper_class]
            paper_exists = instance_exists(g, paper_uri)

            # Si el paper no existe, lo agregamos a la ontología
            if not paper_exists:
                g.add((paper_uri, RDF.type, UEV.Paper))

                # Agrega los valores de las propiedades del paper a la ontología
                # Con tal de que no sean vacíos o '' (en cuyo caso no se agregan)
                if paper_content.get('paper_title', '') != '':
                    g.add((paper_uri, UEV.Title, Literal(paper_content.get('paper_title', ''))))
                if paper_content.get('paper_abstract', '') != '':
                    g.add((paper_uri, UEV.Abstract, Literal(paper_content.get('paper_abstract', ''))))
                if paper_content.get('paper_introduction', '') != '':
                    g.add((paper_uri, UEV.Introduction, Literal(paper_content.get('paper_introduction', ''))))
                if paper_content.get('paper_conclusions', '') != '':
                    g.add((paper_uri, UEV.Conclusion, Literal(paper_content.get('paper_conclusion', ''))))
                if paper_content.get('paper_publication_date', '') != '' and paper_content.get('paper_publication_date', '') is not None:
                    paper_date = format_date(paper_content.get('paper_publication_date', ''))
                    g.add((paper_uri, UEV.Publication_Date, Literal(paper_date, datatype=XSD.date)))
                if paper_content.get('paper_downloaded_pdf', '') != '':
                    g.add((paper_uri, UEV.Paper_pdf, Literal(paper_content.get('paper_downloaded_pdf', ''))))

            # Iteramos sobre cada keyword del paper
            keywords = group_keywords(paper_content.get('paper_keywords', ''))
            for keyword in keywords['entities']:
                keyword_class = keyword.lower().replace(' ', '_')
                # Elimina caracteres ?,\," y ' de la clase
                keyword_class = keyword_class.replace('?', '').replace(',', '').replace('"', '').replace("'", '')
                keyword_uri = UEX[keyword_class]
                keyword_exists = instance_exists(g, keyword_uri)

                # Si la keyword no existe, la agregamos a la ontología
                if not keyword_exists:
                    g.add((keyword_uri, RDF.type, UEV.ConceptAnnotation))

                # Relacionamos el paper con la keyword
                g.add((paper_uri, UEV.hasConcept_Annotation, keyword_uri))

            # Iteramos sobre cada autor del paper
            for author in paper_content.get('paper_authors', []):
                author_class = author.get('paper_author_forename', '') + ' ' + author.get('paper_author_surname', '')
                # print('ACÁ AUTHOR!!', author_class)
                # print('ACÁ AUTHOR!!', author)
                if author_class != ' ' and author_class is not None:
                    # pasar a minúsculas y reemplazar espacios por guiones bajos
                    author_class = author_class.lower().replace(' ', '_')
                    # Elimina caracteres ?,\," y ' de la clase
                    author_class = author_class.replace('?', '').replace(',', '').replace('"', '').replace("'", '')
                    author_uri = UEX[author_class]
                    author_exists = instance_exists(g, author_uri)

                    # Si el autor no existe, lo agregamos a la ontología
                    if not author_exists:
                        g.add((author_uri, RDF.type, UEV.Author))

                        # Agrega los valores de las propiedades del autor a la ontología
                        # Con tal de que no sean vacíos o '' (en cuyo caso no se agregan)
                        if author.get('paper_author_forename', '') != '':
                            g.add((author_uri, UEV.Forename, Literal(author.get('paper_author_forename', ''))))
                        if author.get('paper_author_surname', '') != '':
                            g.add((author_uri, UEV.Surname, Literal(author.get('paper_author_surname', ''))))
                        if author.get('paper_author_email', '') != '':
                            g.add((author_uri, UEV.Email, Literal(author.get('paper_author_email', ''))))
                        if author.get('paper_author_affiliation', '') != '':
                            g.add((author_uri, UEV.Affiliation, Literal(author.get('paper_author_affiliation', ''))))
                        if author.get('paper_author_address_line', '') != '':
                            g.add((author_uri, UEV.Address_Line, Literal(author.get('paper_author_address_line', ''))))
                        if author.get('paper_author_post_code', '') != '':
                            g.add((author_uri, UEV.Post_code, Literal(author.get('paper_author_post_code', ''))))
                        if author.get('paper_author_settlement', '') != '':
                            g.add((author_uri, UEV.Settlement, Literal(author.get('paper_author_settlement', ''))))
                        if author.get('paper_author_country', '') != '' and author.get('paper_author_country', '') is not None:
                            #pasar a minúsculas y reemplazar espacios por guiones bajos
                            author_country = author.get('paper_author_country', '').lower().replace(' ', '_')
                            # Elimina caracteres ?,\," y ' de la clase
                            author_country = author_country.replace('?', '').replace(',', '').replace('"', '').replace("'", '')
                            # Se crea un URI para el país del autor
                            country_uri = UEX[author_country]

                            # Si el país no existe, lo agregamos a la ontología
                            if not instance_exists(g, country_uri):
                                g.add((country_uri, RDF.type, UEV.Country))

                            # Revisa que la propiedad con esos valores no exista ya
                            if not (author_uri, UEV.hasCountry, country_uri) in g:
                                g.add((author_uri, UEV.hasCountry, country_uri))

                    # Relacionamos el autor con el paper
                    g.add((author_uri, UEV.isAuthorOf, paper_uri))

            # Iteramos sobre cada referencia del paper
            for reference in paper_content.get('paper_references', []):
                reference_class = reference.get('reference_paper_title', '')
                # pasar a minúsculas y reemplazar espacios por guiones bajos
                reference_class = reference_class.lower().replace(' ', '_')
                # Elimina caracteres ?,\," y ' de la clase
                reference_class = reference_class.replace('?', '').replace(',', '').replace('"', '').replace("'", '')
                # Revisa que la referencia no tenga el mismo nombre que el paper
                if reference_class != paper_class and reference_class != '' and reference_class is not None:
                    reference_uri = UEX[reference_class]
                    reference_exists = instance_exists(g, reference_uri)

                    # Si la referencia no existe, la agregamos a la ontología
                    if not reference_exists:
                        g.add((reference_uri, RDF.type, UEV.Reference))

                        # Agrega los valores de las propiedades de la referencia a la ontología
                        # Con tal de que no sean vacíos o '' (en cuyo caso no se agregan)
                        if reference.get('reference_paper_title', '') != '':
                            g.add((reference_uri, UEV.Title, Literal(reference.get('reference_paper_title', ''))))
                        if reference.get('reference_paper_publication_date', '') != '':
                            g.add((reference_uri, UEV.Publication_Date, Literal(reference.get('reference_paper_publication_date', ''), datatype=XSD.string)))
                        if reference.get('reference_paper_meeting', '') != '' and reference.get('reference_paper_meeting', '') is not None:
                            # pasar a minúsculas y reemplazar espacios por guiones bajos
                            meeting_class = reference.get('reference_paper_meeting', '').lower().replace(' ', '_')
                            # Elimina caracteres ?,\," y ' de la clase
                            meeting_class = meeting_class.replace('?', '').replace(',', '').replace('"', '').replace("'", '')
                            # Se crea un URI para la conferencia de la referencia
                            meeting_uri = UEX[meeting_class]

                            # Si la conferencia no existe, la agregamos a la ontología
                            if not instance_exists(g, meeting_uri):
                                g.add((meeting_uri, RDF.type, UEV.Meeting))

                            g.add((reference_uri, UEV.hasMeeting, meeting_uri))

                        if reference.get('reference_paper_city', '') != '' and reference.get('reference_paper_city', '') is not None:
                            # pasar a minúsculas y reemplazar espacios por guiones bajos
                            city_class = reference.get('reference_paper_city', '').lower().replace(' ', '_')
                            # Elimina caracteres ?,\," y ' de la clase
                            city_class = city_class.replace('?', '').replace(',', '').replace('"', '').replace("'", '')
                            # Se crea un URI para la ciudad de la referencia
                            city_uri = UEX[city_class]

                            # Si la ciudad no existe, la agregamos a la ontología
                            if not instance_exists(g, city_uri):
                                g.add((city_uri, RDF.type, UEV.City))

                            g.add((reference_uri, UEV.hasCity, city_uri))

                        if reference.get('reference_paper_country', '') != '' and reference.get('reference_paper_country', '') is not None:
                            # pasar a minúsculas y reemplazar espacios por guiones bajos
                            country_class = reference.get('reference_paper_country', '').lower().replace(' ', '_')
                            # Elimina caracteres ?,\," y ' de la clase
                            country_class = country_class.replace('?', '').replace(',', '').replace('"', '').replace("'", '')
                            # Se crea un URI para el país de la referencia
                            country_uri = UEX[country_class]

                            # Si el país no existe, lo agregamos a la ontología
                            if not instance_exists(g, country_uri):
                                g.add((country_uri, RDF.type, UEV.Country))

                            g.add((reference_uri, UEV.hasCountry, country_uri))

                        #if reference.get('reference_paper_note', '') != '':
                        #    g.add((reference_uri, UEV.Note, Literal(reference.get('reference_paper_note', ''))))

                    # Relacionamos el paper con la referencia
                    g.add((paper_uri, UEV.hasReference, reference_uri))


                    # Iteramos sobre los autores de las referencias
                    for ref_author in reference.get('reference_paper_authors', []):
                        ref_author_class = ref_author.get('reference_paper_author_forename', '') + ' ' + ref_author.get('reference_paper_author_surname', '')
                        if ref_author_class != ' ' and ref_author_class is not None:
                            # pasar a minúsculas y reemplazar espacios por guiones bajos
                            ref_author_class = ref_author_class.lower().replace(' ', '_')
                            # Elimina caracteres ?,\," y ' de la clase
                            ref_author_class = ref_author_class.replace('?', '').replace(',', '').replace('"', '').replace("'", '')
                            ref_author_uri = UEX[ref_author_class]
                            ref_author_exists = instance_exists(g, ref_author_uri)

                            # Si el autor de la referencia no existe, lo agregamos a la ontología
                            if not ref_author_exists:
                                g.add((ref_author_uri, RDF.type, UEV.Author))

                                # Agrega los valores de las propiedades del autor de la referencia a la ontología
                                # Con tal de que no sean vacíos o '' (en cuyo caso no se agregan)
                                if ref_author.get('reference_paper_author_forename', '') != '':
                                    g.add((ref_author_uri, UEV.Forename, Literal(ref_author.get('reference_paper_author_forename', ''))))
                                if ref_author.get('reference_paper_author_surname', '') != '':
                                    g.add((ref_author_uri, UEV.Surname, Literal(ref_author.get('reference_paper_author_surname', ''))))

                            # Relacionamos la referencia con el autor hasAuthor
                            g.add((ref_author_uri, UEV.isAuthorOf, reference_uri))
                            
    return g

def validate_shape(datos_graph):
    conforms, v_graph, v_text = validate(datos_graph, shacl_graph=SHAPE_GRAPH, inference='rdfs', serialize_report_graph=True)

    print("Conforma:", conforms)
    if not conforms:
        print("Reporte de validación:\n", v_text)
        
    return conforms
