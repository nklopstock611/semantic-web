from rdflib import Graph, Literal, RDF, URIRef, Namespace, BNode, XSD, Bag, Seq
from rdflib.namespace import RDF, RDFS, OWL

g = Graph()

# Definición de los prefijos de los espacios de nombres
g.bind('rdf', RDF)
g.bind('rdfs', RDFS)
g.bind('owl', OWL)
g.bind("xsd", XSD)

# Definición de los prefijos de ontologías y recursos
UEX = Namespace("http://www.uniandes.web.semantica.example.org/")
UEV = Namespace("http://www.uniandes.web.semantica.ejemplo.org/voca#")
g.bind('uex', UEX)
g.bind('uev', UEV)

def main():
    # Clases principales
    g.add((UEV.Paper, RDF.type, RDFS.Class))
    g.add((UEV.Author, RDF.type, RDFS.Class))
    g.add((UEV.Reference, RDF.type, RDFS.Class))

    # Clases para el futuro
    g.add((UEV.ConceptAnnotation, RDF.type, RDFS.Class))
    g.add((UEV.Country, RDF.type, RDFS.Class))
    g.add((UEV.City, RDF.type, RDFS.Class))
    g.add((UEV.Meeting, RDF.type, RDFS.Class))

    g.add((UEV.Reference, RDFS.subClassOf, UEV.Paper))

    # Valores de Paper
    g.add((UEV.Text, RDF.type, RDF.Property))
    g.add((UEV.Title, RDF.type, RDF.Property))
    g.add((UEV.Abstract, RDF.type, RDF.Property))
    g.add((UEV.Introduction, RDF.type, RDF.Property))
    g.add((UEV.Conclusion, RDF.type, RDF.Property))

    g.add((UEV.hasConcept_Annotation, RDF.type, RDF.Property)) # Clase futura
    g.add((UEV.Publication_Date, RDF.type, RDF.Property))

    # Valores de Author
    g.add((UEV.Forename, RDF.type, RDF.Property))
    g.add((UEV.Surname, RDF.type, RDF.Property))
    g.add((UEV.Email, RDF.type, RDF.Property))
    g.add((UEV.Affiliation, RDF.type, RDF.Property))
    g.add((UEV.Address_Line, RDF.type, RDF.Property))
    g.add((UEV.Post_code, RDF.type, RDF.Property))
    g.add((UEV.Settlement, RDF.type, RDF.Property))
    g.add((UEV.hasCountry, RDF.type, RDF.Property)) # Clase futura

    # Valores especificos de referencias
    g.add((UEV.hasMeeting, RDF.type, RDF.Property)) # Clase futura
    g.add((UEV.hasCity, RDF.type, RDF.Property)) # Clase futura
    g.add((UEV.Note, RDF.type, RDF.Property))

    # Relaciones
    g.add((UEV.hasAuthor, RDF.type, RDF.Property))
    g.add((UEV.hasReference, RDF.type, RDF.Property))
    g.add((UEV.isAuthorOf, RDF.type, RDF.Property))
    g.add((UEV.isReferencedBy, RDF.type, RDF.Property))

    # Subpropiedades
    g.add((UEV.Title, RDFS.subPropertyOf, UEV.Text))
    g.add((UEV.Abstract, RDFS.subPropertyOf, UEV.Text))
    g.add((UEV.Concept_Annotation, RDFS.subPropertyOf, UEV.Text))
    g.add((UEV.Introduction, RDFS.subPropertyOf, UEV.Text))
    g.add((UEV.Conclusion, RDFS.subPropertyOf, UEV.Text))

    # Texto 
    g.add((UEV.Text, RDFS.domain, UEV.Paper))
    g.add((UEV.Text, RDFS.range, XSD.string))
    # Title
    g.add((UEV.Title, RDFS.domain, UEV.Paper))
    g.add((UEV.Title, RDFS.range, XSD.string))
    # Abstract
    g.add((UEV.Abstract, RDFS.domain, UEV.Paper))
    g.add((UEV.Abstract, RDFS.range, XSD.string))
    # Introduction
    g.add((UEV.Introduction, RDFS.domain, UEV.Paper))
    g.add((UEV.Introduction, RDFS.range, XSD.string))
    # Conclusion
    g.add((UEV.Conclusion, RDFS.domain, UEV.Paper))
    g.add((UEV.Conclusion, RDFS.range, XSD.string))
    # Concept_Anotation
    g.add((UEV.hasConcept_Annotation, RDFS.domain, UEV.Paper))
    g.add((UEV.hasConcept_Annotation, RDFS.range, UEV.ConceptAnnotation))
    # Publication_Date (Puede tener año, año-mes o año-mes-día) -- Revisar si es posible estandarizar formato y pasar a date
    g.add((UEV.Publication_Date, RDFS.domain, UEV.Paper))
    g.add((UEV.Publication_Date, RDFS.range, XSD.string))

    # Forename
    g.add((UEV.Forename, RDFS.domain, UEV.Author))
    g.add((UEV.Forename, RDFS.range, XSD.string))
    # Surname
    g.add((UEV.Surname, RDFS.domain, UEV.Author))
    g.add((UEV.Surname, RDFS.range, XSD.string))
    # Email
    g.add((UEV.Email, RDFS.domain, UEV.Author))
    g.add((UEV.Email, RDFS.range, XSD.string))
    # Affiliation
    g.add((UEV.Affiliation, RDFS.domain, UEV.Author))
    g.add((UEV.Affiliation, RDFS.range, XSD.string))
    # Address_Line
    g.add((UEV.Address_Line, RDFS.domain, UEV.Author))
    g.add((UEV.Address_Line, RDFS.range, XSD.string))
    # Post_code -- Puede ser numero
    g.add((UEV.Post_code, RDFS.domain, UEV.Author))
    g.add((UEV.Post_code, RDFS.range, XSD.string))
    # Settlement
    g.add((UEV.Settlement, RDFS.domain, UEV.Author))
    g.add((UEV.Settlement, RDFS.range, XSD.string))
    # Country -- Pensar modelarlo como clase
    g.add((UEV.hasCountry, RDFS.domain, UEV.Author))
    g.add((UEV.hasCountry, RDFS.range, UEV.Country))
    # Meeting
    g.add((UEV.hasMeeting, RDFS.domain, UEV.Reference))
    g.add((UEV.hasMeeting, RDFS.range, UEV.Meeting))
    # City -- Pensar modelarlo como clase
    g.add((UEV.hasCity, RDFS.domain, UEV.Reference))
    g.add((UEV.hasCity, RDFS.range, UEV.City))
    # Note
    g.add((UEV.Note, RDFS.domain, UEV.Reference))
    g.add((UEV.Note, RDFS.range, XSD.string))

    # Relaciones
    g.add((UEV.hasAuthor, RDFS.domain, UEV.Paper))
    g.add((UEV.hasAuthor, RDFS.range, UEV.Author))

    g.add((UEV.hasReference, RDFS.domain, UEV.Paper))
    g.add((UEV.hasReference, RDFS.range, UEV.Reference))

    g.add((UEV.isAuthorOf, RDFS.domain, UEV.Author))
    g.add((UEV.isAuthorOf, RDFS.range, UEV.Paper))

    g.add((UEV.isReferencedBy, RDFS.domain, UEV.Reference))
    g.add((UEV.isReferencedBy, RDFS.range, UEV.Paper))

    # Clases Disjuntas
    g.add((UEV.Paper, OWL.disjointWith, UEV.Author))

    # Restricciones Texto Functional Property
    # TODO: ...

    
