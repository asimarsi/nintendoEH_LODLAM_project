from lxml import etree as ET
from rdflib import Graph, Namespace, URIRef, RDF, RDFS, OWL, Literal
from rdflib.namespace import XSD, SKOS

def resolve_uri(value, LOCAL, namespaces_dict):
    if value.startswith('#'):
        return LOCAL[value[1:]] 
    elif ':' in value and not value.startswith('http'):
        prefix, local_name = value.split(':', 1)
        if prefix in namespaces_dict:
            return namespaces_dict[prefix][local_name]
    return URIRef(value)

def extract_rdf_from_tei(xml_file_path):

    g = Graph() # graph creation
    
    # Used namespace definitions for Nintendo project
    DCTERMS = Namespace("http://purl.org/dc/terms/")
    FRBROO = Namespace("http://iflastandards.info/ns/fr/frbr/frbroo/")
    SCHEMA = Namespace("https://schema.org/")
    CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
    SKOS_NS = Namespace("http://www.w3.org/2004/02/skos/core#")
    
    # Local namespace for the RDF dataset generated from the TEI XML
    LOCAL = Namespace("https://w3id.org/nintendo/")    
    
    # Namespace dictionary for binding prefixes to URIs in the RDF graph
    namespaces_dict = {
        "dcterms": DCTERMS,
        "frbroo": FRBROO,
        "schema": SCHEMA,
        "crm": CRM,
        "skos": SKOS_NS,
        "rdf": RDF,
        "rdfs": RDFS,
        "owl": OWL
    }
    
    # Bind every prefix to the corresponding URI in the RDF graph
    for prefix, uri in namespaces_dict.items():
        g.bind(prefix, uri, override=True)
    g.bind("nintendo", LOCAL, override=True)
    
    tree = ET.parse(xml_file_path) # parsing using lxml
    root = tree.getroot()
    
    # Dictionary for the namespaces used in the TEI XML document
    nsmap = {
        'tei': 'http://www.tei-c.org/ns/1.0',
        'xml': 'http://www.w3.org/XML/1998/namespace'
    }
    
    # 1. Automatic extraction of elements with @sameAs attributes to generate owl:sameAs triples
    elements_with_sameas = root.xpath('//*[@xml:id and @sameAs]', namespaces=nsmap)
    
    for el in elements_with_sameas:
        xml_id = el.get('{http://www.w3.org/XML/1998/namespace}id')
        same_as = el.get('sameAs')
        
        subj = LOCAL[xml_id]
        obj = URIRef(same_as)
        g.add((subj, OWL.sameAs, obj))
        
    # 2. Extraction of <relation> elements from <relationGrp> in <standOff>
    relations = root.xpath('.//tei:relationGrp/tei:relation', namespaces=nsmap)
    
    for relation in relations:
        active = relation.get('active')
        name = relation.get('name')
        passive = relation.get('passive')
        
        if active and name and passive:
            subj = resolve_uri(active, LOCAL, namespaces_dict)
            pred = resolve_uri(name, LOCAL, namespaces_dict)
            obj = resolve_uri(passive, LOCAL, namespaces_dict)
            g.add((subj, pred, obj))
    
    # 3. Extraction of Person Names (<persName>)
    for person in root.xpath('.//tei:person[@xml:id]', namespaces=nsmap):
        p_id = person.get("{http://www.w3.org/XML/1998/namespace}id")
        subject_uri = LOCAL[p_id]
        
        name_tag = person.find('./tei:persName', namespaces=nsmap)
        if name_tag is not None:
            raw_text = "".join(name_tag.itertext())
            full_name = " ".join(raw_text.split())
            if full_name:
                g.add((subject_uri, RDFS.label, Literal(full_name, lang="en")))

    # 4. Extraction of Organizations (<orgName>)
    for org in root.xpath('.//tei:org[@xml:id]', namespaces=nsmap):
        o_id = org.get("{http://www.w3.org/XML/1998/namespace}id")
        subject_uri = LOCAL[o_id]
        
        org_tag = org.find('./tei:orgName', namespaces=nsmap)
        if org_tag is not None and org_tag.text:
            g.add((subject_uri, RDFS.label, Literal(org_tag.text.strip(), lang="en")))

    # 5. Extraction of Places (<placeName>)
    for place in root.xpath('.//tei:place[@xml:id]', namespaces=nsmap):
        pl_id = place.get("{http://www.w3.org/XML/1998/namespace}id")
        subject_uri = LOCAL[pl_id]
        
        place_tag = place.find('./tei:placeName', namespaces=nsmap)
        if place_tag is not None and place_tag.text:
            g.add((subject_uri, RDFS.label, Literal(place_tag.text.strip(), lang="en")))

    # 6. Extraction of Objects / Hardware (<objectIdentifier>)
    for obj in root.xpath('.//tei:object[@xml:id]', namespaces=nsmap):
        obj_id = obj.get("{http://www.w3.org/XML/1998/namespace}id")
        subject_uri = LOCAL[obj_id]
        
        obj_tag = obj.find('./tei:objectIdentifier', namespaces=nsmap)
        if obj_tag is not None and obj_tag.text:
            g.add((subject_uri, RDFS.label, Literal(obj_tag.text.strip(), lang="en")))

    # 7. Extraction of Bibliographic Works (<title> & <date>)
    for bibl in root.xpath('.//tei:bibl[@xml:id]', namespaces=nsmap):
        b_id = bibl.get("{http://www.w3.org/XML/1998/namespace}id")
        subject_uri = LOCAL[b_id]
        
        title_tag = bibl.find('./tei:title', namespaces=nsmap)
        if title_tag is not None and title_tag.text:
            g.add((subject_uri, DCTERMS.title, Literal(title_tag.text.strip(), lang="en")))
            
        date_tag = bibl.find('./tei:date', namespaces=nsmap)
        if date_tag is not None:
            year_val = date_tag.get("when")
            if year_val:
                year_val = year_val.strip()
                if len(year_val) == 4:
                    date_value = Literal(year_val, datatype=XSD.gYear)
                else:
                    date_value = Literal(year_val, datatype=XSD.date)
                g.add((subject_uri, DCTERMS.date, date_value))

    # 8. Extraction of Concepts (<term>)
    for concept in root.xpath('.//tei:list[@type="concepts"]/tei:item[@xml:id]', namespaces=nsmap):
        c_id = concept.get("{http://www.w3.org/XML/1998/namespace}id")
        subject_uri = LOCAL[c_id]
        
        term_tag = concept.find('./tei:term', namespaces=nsmap)
        if term_tag is not None and term_tag.text:
            g.add((subject_uri, SKOS_NS.prefLabel, Literal(term_tag.text.strip(), lang="en")))

    # 9. Extraction of Historical Events (<label> & <date>)
    for event in root.xpath('.//tei:event[@xml:id]', namespaces=nsmap):
        e_id = event.get("{http://www.w3.org/XML/1998/namespace}id")
        subject_uri = LOCAL[e_id]
        
        label_tag = event.find('./tei:label', namespaces=nsmap)
        if label_tag is not None and label_tag.text:
            g.add((subject_uri, RDFS.label, Literal(label_tag.text.strip(), lang="en")))
            
        date_tag = event.find('./tei:date', namespaces=nsmap)
        if date_tag is not None:
            year_val = date_tag.get("when")
            if year_val:
                g.add((subject_uri, DCTERMS.date, Literal(year_val.strip(), datatype=XSD.gYear)))
            
    return g

if __name__ == "__main__":
    # Aggiorna il percorso se il file XML si trova in una sottocartella
    file_input = "nintendoHE.xml" 
    
    result_graph = extract_rdf_from_tei(file_input)
    
    # Serializzazione in formato Turtle (.ttl)
    turtle_data = result_graph.serialize(format="turtle")
    
    # Salvataggio nel file di output
    with open("dataset.ttl", "w", encoding="utf-8") as f:
        f.write(turtle_data)
        
    print("Dataset RDF/Turtle generato con successo e salvato in dataset.ttl!")