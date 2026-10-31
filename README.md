# Nintendo Entertainment Heritage

From traditional playing cards to video games: exploring connections across Nintendo’s entertainment history.

**Nintendo Entertainment Heritage** is a cultural heritage and Linked Open Data project guided by the research question:

> **How can the connections between Nintendo’s products, people, characters and places help us understand continuity and change in its entertainment history?**

Starting from selected passages of the English Wikipedia article [History of Nintendo](https://en.wikipedia.org/w/index.php?title=History_of_Nintendo&oldid=1382723079), the project explores two paths:

- **Mario and Jumpman:** connecting Donkey Kong (1981) and Mario Bros. (1983) through the same character and one of his historical names.
- **Hanafuda and Pokémon Trading Card Game:** comparing physical card play across different periods. This is a thematic interpretation, not a claim that Pokémon cards developed directly from Hanafuda.

The workflow combines source selection, theoretical modelling, conceptual diagrams created with Graffoo in yEd, TEI/XML encoding, HTML transformation and RDF export.

The project reuses CIDOC CRM, FRBRoo, Schema.org, SKOS and Dublin Core Terms. A minimal local vocabulary defines the property `neh:featuresCharacter`.

The catalogue contains **22 main entities and 12 supporting records**. The RDF dataset contains **330 triples**, including the 71 explicit statements recorded in the TEI.

[Explore the project website](https://asimarsi.github.io/nintendoEH_LODLAM_project/)

## Main files

| File or folder | Content |
| --- | --- |
| `index.html` | Project report and presentation |
| `assets/` | Styles, JavaScript, fonts, images and diagrams |
| `nintendoHE.xml` | Selected source text and TEI catalogue |
| `html/nintendoHE.html` | HTML edition generated from the TEI |
| `dataset.ttl` | Complete RDF dataset |
| `ontology.ttl` | Local project vocabulary |
| `transform.py`, `transform.xslt` | TEI-to-HTML transformation |
| `tei_to_rdf.py` | TEI-to-RDF transformation |
| `rdf_*.ttl` | Selected RDF visualization extracts |
| `visualization_extracts.zip` | Visualization extracts and their generation script |

## Reproducing the transformations

Install the Python dependencies:

```bash
python3 -m pip install lxml rdflib
```

From the project root, run:

```bash
python3 transform.py
python3 tei_to_rdf.py
```

The first command generates `html/nintendoHE.html`; the `html` folder must exist.

The second command generates `dataset.ttl` beside the XML file.

To reproduce the visualization extracts, unpack `visualization_extracts.zip` into a separate folder, then run from the project root:

```bash
python3 path/to/extracted-folder/prepare_rdf_views.py dataset.ttl
```

Replace `path/to/extracted-folder` with the actual folder path. The extracts are saved beside the extraction script; the complete dataset remains unchanged.

Use [RDF Grapher](https://www.ldf.fi/service/rdf-grapher) with Turtle input and SVG output to visualize the extracts.

## Sources and credits

The Wikipedia text retains its attribution under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The TEI header identifies the source revision and explains the selection criteria. Additional evidence is documented in the catalogue.

Image sources and available licence information are listed on the website and in `assets/image-credits.json`. Images and fonts retain their respective terms.

AI assistance for code, text, diagrams and technical checks is acknowledged on the website.

## Academic context

Individual project for **Information Science and Cultural Heritage**, academic year **2025–2026**, University of Bologna.

Author: [Asia Marselli](https://github.com/asimarsi)
