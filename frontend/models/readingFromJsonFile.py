import json
import re

SAMPLE_ITEMS: json

with open('testData.json') as jsonFile:
    SAMPLE_ITEMS = json.load(jsonFile)

sections = set()
for j in SAMPLE_ITEMS:
    sectionNameSeperated = sectionNameSeperated = re.sub(r"(\w)([A-Z])", r"\1 \2", j['resourceType'])
    j['resourceType'] = sectionNameSeperated
    sections.add(j['resourceType'])
    
LIST_OF_SECTIONS = sorted(sections)