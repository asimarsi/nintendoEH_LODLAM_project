"""Convert the essential Nintendo TEI catalogue into RDF/Turtle.

Requirements: pip install lxml rdflib
Run: python tei_to_rdf.py nintendoHE_essential.xml
With no argument, the input is nintendoHE.xml. Output: dataset.ttl.
"""

from pathlib import Path
import sys
from lxml import etree as ET
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS
from rdflib.namespace import DCTERMS, SKOS, XSD

TEI = {"tei": "http://www.tei-c.org/ns/1.0"}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"


def text_of(element):
    """Read text even when it contains nested TEI tags."""
    return " ".join("".join(element.itertext()).split())


def resolve_uri(value, local, prefixes):
    """Expand #local identifiers, full URLs and declared prefixes."""
    if value.startswith("#"):
        return local[value[1:]]
    if value.startswith(("https://", "http://")):
        return URIRef(value)
    prefix, name = value.split(":", 1)
    return URIRef(prefixes[prefix] + name)


def date_literal(value):
    """Keep the precision stated by the source: year, month or day."""
    datatype = {4: XSD.gYear, 7: XSD.gYearMonth, 10: XSD.date}
    return Literal(value, datatype=datatype[len(value)])


def extract_rdf_from_tei(xml_file_path):
    # 1. Read the XML and the URI settings declared in its header.
    root = ET.parse(str(xml_file_path))
    base = root.find(".//tei:idno[@type='rdf_resource_base']", TEI)
    if base is None or not base.text:
        raise ValueError("The TEI header must declare rdf_resource_base.")
    local = Namespace(base.text.strip())
    prefixes = {}
    for definition in root.findall(".//tei:prefixDef", TEI):
        prefixes[definition.get("ident")] = definition.get("replacementPattern").replace("$1", "")

    graph = Graph()
    graph.bind("nintendo", local)
    graph.bind("dcterms", DCTERMS)
    graph.bind("rdfs", RDFS)
    for prefix, uri in prefixes.items():
        graph.bind(prefix, Namespace(uri))

    # 2. Copy explicit relations, including rdf:type class declarations.
    relations = root.findall(".//tei:standOff/tei:listRelation/tei:relation", TEI)
    for relation in relations:
        subject = resolve_uri(relation.get("active"), local, prefixes)
        predicate = resolve_uri(relation.get("name"), local, prefixes)
        object_uri = resolve_uri(relation.get("passive"), local, prefixes)
        graph.add((subject, predicate, object_uri))

    # 3. Label every main/support record and the supplementary source records.
    # Restrict extraction to the catalogue: source-text mentions are not new entities.
    records = root.xpath("//tei:standOff//*[@n='main' or @n='support'] | "
                         "//tei:standOff/tei:listBibl[@type='evidence_sources']/tei:bibl",
                         namespaces=TEI)
    wiki_source = root.find(".//tei:sourceDesc/tei:bibl[@type='source_text']", TEI)
    if wiki_source is not None:
        records.append(wiki_source)

    for record in records:
        subject = local[record.get(XML_ID)]
        names = record.xpath("tei:persName | tei:orgName | tei:placeName | tei:title | tei:label", namespaces=TEI)
        if names:
            label = Literal(text_of(names[0]), lang="en")
            graph.add((subject, RDFS.label, label))
            if (subject, RDF.type, SKOS.Concept) in graph:
                graph.add((subject, SKOS.prefLabel, label))
            if record.tag == "{http://www.tei-c.org/ns/1.0}bibl":
                graph.add((subject, DCTERMS.title, label))

        # 4. Authority links are seeAlso references, not identity assertions.
        for link in record.findall("tei:note[@type='authority_reference']/tei:ref", TEI):
            graph.add((subject, RDFS.seeAlso, URIRef(link.get("target"))))
        for link in record.findall("tei:ref", TEI):
            graph.add((subject, RDFS.seeAlso, URIRef(link.get("target"))))
        for evidence in record.get("source", "").split():
            graph.add((subject, DCTERMS.source, resolve_uri(evidence, local, prefixes)))

        # 5. Export work release dates and event dates as typed literals.
        for date in record.findall("tei:date[@type='first_release']", TEI):
            graph.add((subject, DCTERMS.issued, date_literal(date.get("when"))))
        if record.get("when"):
            graph.add((subject, DCTERMS.date, date_literal(record.get("when"))))

        # 6. Keep regional launches and dated roles as readable descriptions.
        # This avoids new event/role nodes and preserves their territory/context.
        # Exact structured attributes and per-relation evidence remain in the TEI.
        for note in record.xpath("tei:note[not(@type='authority_reference')] | tei:desc", namespaces=TEI):
            graph.add((subject, DCTERMS.description, Literal(text_of(note), lang="en")))
        for affiliation in record.findall("tei:affiliation", TEI):
            description = text_of(affiliation) + " at " + affiliation.get("ref", "").lstrip("#")
            if affiliation.get("from"):
                description += "; from " + affiliation.get("from")
            if affiliation.get("to"):
                description += "; to " + affiliation.get("to")
            graph.add((subject, DCTERMS.description, Literal(description, lang="en")))

    return graph


# 7. Run the transformation and write a Turtle file beside the input XML.
if __name__ == "__main__":
    input_path = Path(sys.argv[1] if len(sys.argv) > 1 else "nintendoHE.xml")
    graph = extract_rdf_from_tei(input_path)
    output_path = input_path.with_name("dataset.ttl")
    graph.serialize(destination=str(output_path), format="turtle")
    print(f"Saved {len(graph)} RDF triples to {output_path}")
