# obo-metadata

## Running the scripts

The following are required:
  - [ontofetch](https://github.com/knocean/ontofetch) - for `fetch.py`
  - [PyYAML](https://github.com/yaml/pyyaml) - for `extract.py`
  - [lxml](http://lxml.de/index.html) - for `extract.py`
  
Make sure that ontofetch is added to your PATH variable in order to run `fetch.py`. Please note that `fetch.py` will take about a half hour (or longer) to complete.

Once you've run `fetch.py`, a collection of zipped ontologies will be available in `archive/`. Their corresponding owl:Ontology element will be available in `metadata/xml/`.

To run `extract.py`, populate the `metadata/md/` folder with the [.md files here](https://github.com/OBOFoundry/OBOFoundry.github.io/tree/master/ontology) (to automate later). This will generate two TSVs in the main directory (see below for details).

## Reading the TSVs

`obo_metadata.tsv` contains extracted elements from the .md files available from the OBO Foundry repository. `ont_metadata.tsv` contains the same elements from the released ontology files. Currently, the script extracts the following elements:
  - Title
  - Description
  - License
  
In the owl:Ontology elements from the released ontologies, these should be annotated with Dublin Core properties.

In either file, if an ontology's ID is followed by *, it means that the file does not exist.

In the `ont_metadata.tsv` file, columns with no headers are the `rdfs:comment` fields from the ontology metadata.
