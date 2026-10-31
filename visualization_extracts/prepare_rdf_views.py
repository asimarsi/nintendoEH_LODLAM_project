"""Create small RDF Grapher views without changing the full dataset.
Requirements: pip install rdflib
Run beside dataset.ttl: python prepare_rdf_views.py
Or: python prepare_rdf_views.py path/to/dataset.ttl
"""
from pathlib import Path
import sys
from rdflib import Graph, Namespace, URIRef, RDFS

# 1. Read the complete dataset. The source file is never overwritten.
source = Path(sys.argv[1] if len(sys.argv) > 1 else "dataset.ttl")
full = Graph().parse(source, format="turtle")
LOCAL = Namespace("https://asimarsi.github.io/nintendoEH_LODLAM_project/dataset.ttl#")
output = Path(__file__).resolve().parent

# 2. Select catalogue records by their local identifiers.
# Source records (src_...) and wiki_source are documentation, not view nodes.
records = {
    subject for subject in full.subjects(RDFS.label, None)
    if str(subject).startswith(str(LOCAL))
    and not str(subject)[len(str(LOCAL)):].startswith("src_")
    and subject != LOCAL.wiki_source
}
mario = {LOCAL[name] for name in (
    "work_DonkeyKong", "work_MarioBros", "char_Mario", "name_Jumpman"
)}
cards = {LOCAL[name] for name in (
    "type_Hanafuda", "franchise_Pokemon", "game_PokemonTCG",
    "concept_PlayingCards", "concept_CardGame", "concept_CollectibleCardGame"
)}

# 3. Keep only existing links between the selected records and their labels.
# Classes, long descriptions, dates and evidence links remain in the full dataset.
for filename, selected in (
    ("rdf_overview.ttl", records),
    ("rdf_mario_jumpman.ttl", mario),
    ("rdf_hanafuda_pokemon.ttl", cards),
):
    view = Graph()
    for prefix, uri in full.namespaces():
        view.bind(prefix, uri)
    for subject, predicate, object_value in full:
        if subject in selected and (
            predicate == RDFS.label
            or isinstance(object_value, URIRef) and object_value in selected
        ):
            view.add((subject, predicate, object_value))
    assert set(view).issubset(set(full))
    destination = output / filename
    assert destination.resolve() != source.resolve()
    view.serialize(destination=str(destination), format="turtle")
    print(f"{filename}: {len(view)} triples")
