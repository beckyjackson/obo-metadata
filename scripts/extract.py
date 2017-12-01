import codecs
from lxml import etree
import os.path
import pprint as pp
import yaml

# vars
md_tsv_path = "../obo_metadata.tsv"
xml_tsv_path = "../ont_metadata.tsv"
fname = "obo_foundry.txt"

# functs
def toTSV (field):
	tab = "\t"
	if field:
		return field.replace('\n', ' ') + tab
	else:
		return tab

def write(path, tsv_lines):
	with codecs.open(path, 'w', 'utf-8') as f:
		f.write('ID\tTitle\tDescription\tLicense\n')
		for line in tsv_lines:
			f.write("%s\n" % line)

# -----------------------------------------------------------

with open(fname) as f:
	ontologies = f.read().splitlines()

md_details = []
xml_details = []

for ont in ontologies:
	# Get the OBO metadata
	md_name = "../metadata/md/" + ont + ".md"
	if os.path.isfile(md_name):	
		with open(md_name) as m:
			# Extract YAML
			flag = False
			data = []
			for line in m:
				if flag and line.startswith('---'):
					flag = False
					break
				if not flag and line.startswith('---'):
					flag = True
				if flag:
					data.append(line)

			# Remove first ----
			data.pop(0)
			# Turn into dictionary & get desired details
			md = yaml.load(''.join(data))
			md_extract = {'id': ont,
					      'title': md.get('title'),
					      'description': md.get('description'),
					      'license': md.get('license')}
			# Add to details
			md_details.append(md_extract)
	# File does not exist
	else:
		# Add a * to denote there is no OBO metadata
		md_extract = {'id': ont + "*",
					  'title': None,
					  'description': None,
					  'license': None}
		# Add to details
		md_details.append(md_extract)

	# Get the owl:Ontology metadata
	xml_name = "../metadata/xml/" + ont + "-element.owl"
	if os.path.isfile(xml_name):
		p = etree.XMLParser(recover=True)
		xml = etree.parse(xml_name, parser=p)

		# Iterate through xml to find details
		title = None
		description = None
		license = None
		comments = []
		for el in xml.iter():
			if el.tag == '{http://purl.org/dc/elements/1.1/}license':
				license = el.text
			if el.tag == '{http://purl.org/dc/elements/1.1/}description':
				description = el.text
			if el.tag == '{http://purl.org/dc/elements/1.1/}title':
				title = el.text
			if el.tag == '{http://www.w3.org/2000/01/rdf-schema#}comment':
				comments.append(el.text)
		xml_extract = {'id': ont,
					   'title': title,
					   'description': description,
					   'license': license,
					   'comments': comments}
		xml_details.append(xml_extract)

	else:
		# Add a * to denote there is no XML
		xml_extract = {'id': ont + "*",
					   'title': None,
					   'description': None,
					   'license': None,
					   'comments': []}
		xml_details.append(xml_extract)

# Create array of TSV lines for md from YAML
md_tsv = []
for dts in md_details:
	line=toTSV(dts.get('id'))
	line+=toTSV(dts.get('title'))
	line+=toTSV(dts.get('description'))
	if dts.get('license'):
		line+=toTSV(dts.get('license').get('url'))
	else:
		line += "\t"
	md_tsv.append(line)

# Create array of TSV lines for md from XML
xml_tsv = []
for dts in xml_details:
	line=toTSV(dts.get('id'))
	line+=toTSV(dts.get('title'))
	line+=toTSV(dts.get('description'))
	line+=toTSV(dts.get('license'))
	for cmt in dts.get('comments'):
		line+=toTSV(cmt)
	xml_tsv.append(line)

# Finally, write to file
write(md_tsv_path, md_tsv)
write(xml_tsv_path, xml_tsv)
