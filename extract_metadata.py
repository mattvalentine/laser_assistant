"""pulls metadata from svg file"""

import xml.etree.ElementTree as ET
import json


def extract_embeded_model(filename):
    """extracts embeded model if there is one in metadata"""
    model = None
    tree = ET.parse(filename)
    root = tree.getroot()

    for metadata in root.findall('{http://www.w3.org/2000/svg}metadata'):
        lasermetadata = metadata.find(
            '{http://www.w3.org/2000/svg}laserassistant')
        if lasermetadata is not None:
            model = json.loads(lasermetadata.attrib['model'])
    return model


if __name__ == "__main__":
    FILENAME = "switch-with-data.svg"
    METADATA = extract_embeded_model(FILENAME)
    JSON_FILE = open("extracted.json", "w")
    JSON_FILE.write(json.dumps(METADATA, indent=4))
    JSON_FILE.close()
    # print(json.dumps(METADATA, indent=1))
