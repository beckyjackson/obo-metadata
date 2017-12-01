import subprocess

# Get the OBO Foundry ont IDs from file
fname = "obo_foundry.txt"
with open(fname) as f:
	ontologies = f.read().splitlines()

# Download each ontology and store it as a zip in archive
for ont in ontologies:
	print "Fetching " + ont
	cmd = "ontofetch -d ../archive/" + ont + " -p http://purl.obolibrary.org/obo/" + ont + ".owl -z"
	subprocess.call(cmd, shell=True)

# Move the Ontology elements to the XML folder
cmd = "mv ../archive/*-element.owl ../metadata/xml"
subprocess.call(cmd, shell=True)
cmd = "mv catalog.edn .."
subprocess.call(cmd, shell=True)
