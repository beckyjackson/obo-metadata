import os
import shutil
import subprocess

# Get the OBO Foundry ont IDs from file
fname = "obo_foundry.txt"
with open(fname) as f:
	ontologies = f.read().splitlines()

unfetched = []
# Download each ontology and extract the metadata
for ont in ontologies:
	cmd = "ontofetch -d " + ont + " -p http://purl.obolibrary.org/obo/" + ont + ".owl -z" 
	cmd += "; rm -rf " + ont + ".zip; mv " + ont + "-element.owl metadata/xml"
  	subprocess.call(cmd, shell=True)
  	if os.path.isdir(ont):
  		cmd = "rm -rf " + ont
  		subprocess.call(cmd, shell=True)
  		unfetched.append(ont)

print "-----------------------"
print "ONTOLOGIES NOT FETCHED:"
for uf in unfetched:
	print uf
