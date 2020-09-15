"""pulls metadata from svg file"""

import xml.etree.ElementTree as ET
import json
from laser_svg_parser import model_to_svg_file


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
    SVG_MODEL = extract_embeded_model(FILENAME)
    JSON_FILE = open("insert.json", "r")
    NEW_MODEL = json.loads(JSON_FILE.read())
    # print(NEW_MODEL)
    JSON_FILE.close()
    model_to_svg_file(SVG_MODEL, design=NEW_MODEL, filename="updated.svg")
    # print(json.dumps(METADATA, indent=1))
