# svg_parser.py
"""functions to parse specially formatted svg files and
   python dictionary models for laser cutting applications"""

import xml.etree.ElementTree as ET
import json

from laser_svg_utils import (element_to_tree, get_attributes, new_svg_tree,
                             path_string_to_element, tree_to_file)
from laser_path_utils import tree_to_paths, combine_paths, is_inside


def parse_svg_tree(svg_root, attrib):
    """Recursive SVG parser"""
    svg_data = {}
    blank_index = 1
    for item in svg_root:
        if item.tag.endswith("/svg}g"):
            if 'data-name' not in item.attrib:
                item.attrib['data-name'] = f"blank{blank_index}"
                blank_index += 1
                # item.attrib['data-name'] = item.attrib['id']
            name = item.attrib['data-name']
            svg_data[name] = parse_svg_tree(item, attrib)
        else:
            tree = element_to_tree(item, attrib)
            if 'paths' not in svg_data:
                svg_data['paths'] = []
            new_paths = tree_to_paths(tree)
            for path in new_paths:
                svg_data['paths'].append(path)
            if 'style' in item.attrib:
                svg_data['style'] = item.attrib['style']
    return svg_data


def parse_svgfile(filename):
    """Read joints and shapes from specially formatted SVG file."""
    svg_data = {}
    tree = ET.parse(filename)
    attrib = get_attributes(tree)
    svg_data['tree'] = parse_svg_tree(tree.getroot(), attrib)
    svg_data['attrib'] = attrib
    return svg_data


def layer_from_dict(name, sub_tree, svg_root):
    """subfunction to convert dictionary into layer"""
    attrib = {'id': name, 'data-name': name}
    new_layer = ET.Element('g', attrib)
    tree_to_svg(sub_tree, new_layer)
    svg_root.append(new_layer)


def path_from_dict(tree_dict, svg_root):
    """subfunction to convert dictionary into path"""
    paths = combine_paths(tree_dict['paths'])
    style = ""
    if 'style' in tree_dict:
        style = tree_dict['style']
    for path in paths:
        svg_path = path_string_to_element(path, style=style)
        svg_root.append(svg_path)


def tree_to_svg(tree_dict, svg_root):
    """recursively turn dict into SVG layers + paths"""
    for key, value in tree_dict.items():
        if isinstance(value, dict):
            layer_from_dict(key, value, svg_root)
        elif key == 'paths':
            path_from_dict(tree_dict, svg_root)


def model_to_svg_tree(model, design=None):
    """Convert dictionary model with tree + attrib into SVG XML"""
    assert isinstance(model, dict)
    assert 'tree' in model
    assert isinstance(model['tree'], dict)
    assert 'attrib' in model
    assert isinstance(model['attrib'], dict)

    dict_tree = model['tree']
    attrib = model['attrib']

    svg_tree = new_svg_tree(attrib)
    svg_root = svg_tree.getroot()

    if design is None:
        design = model
    embed_model(design, svg_tree)

    tree_to_svg(dict_tree, svg_root)

    return svg_tree


def embed_model(model, tree):
    """embeds a model in an svg tree as metadata"""
    root = tree.getroot()
    metadata = ET.Element("metadata")
    ET.SubElement(metadata, "laserassistant", {"model": json.dumps(model)})
    root.append(metadata)


def model_to_json(model, filename="", indent=None):
    """Converts model to JSON as string or file"""
    json_model = json.dumps(model, indent=indent)
    if filename != "":
        json_file = open(filename, "w")
        json_file.write(json_model)
    return json_model


def model_to_svg_file(model, design=None, filename="output.svg"):
    """Outputs model to SVG file"""
    svg_tree = model_to_svg_tree(model, design=design)
    tree_to_file(svg_tree, filename=filename)


def separate_perims_from_cuts(paths):
    """take a list of paths and returns two lists of paths faces and cuts."""
    perims = []
    cuts = []

    for path in paths:
        inside = False
        for other_path in paths:
            if other_path is not path:
                if is_inside(path, other_path):
                    inside = True
        if inside:
            cuts.append(path)
        else:
            perims.append(path)

    return perims, cuts
