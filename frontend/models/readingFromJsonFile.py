import json

SAMPLE_ITEMS: json
with open('testData.json') as jsonFile:
    SAMPLE_ITEMS = json.load(jsonFile)
