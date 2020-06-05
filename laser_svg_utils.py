# laser_svg_utils.py
"""Utility functions for working with SVGs for laser cutting"""

import xml.etree.ElementTree as ET
import tempfile


def get_attributes(tree):
    """returns attributes of svg tree root"""
    root = tree.getroot()
    attrib = root.attrib
    return attrib


def new_svg_tree(attrib):
    """create a new svg element tree"""
    new_root = ET.Element('svg')
    new_root.attrib = attrib
    if "xmlns" not in new_root.attrib:
        new_root.attrib["xmlns"] = "http://www.w3.org/2000/svg"
    new_tree = ET.ElementTree(new_root)
    return new_tree


def svg_string(tree):
    """convert svg element tree object to a string without namespace junk"""
    root = tree.getroot()
    output_string = ET.tostring(root).decode("utf-8")
    output_string = output_string.replace(
        'xmlns:svg="http://www.w3.org/2000/svg" ', "")
    output_string = output_string.replace("svg:", "")
    return output_string


def element_to_tree(element, attrib):
    """SVG element + attributes = new SVG tree with just that element"""
    tree = new_svg_tree(attrib)
    root = tree.getroot()
    root.append(element)
    return tree


def tree_to_tempfile(tree):
    """turn SVG tree into a tempfile"""
    temp_svg = tempfile.NamedTemporaryFile(suffix=".svg", delete=False)
    svg_bytes = svg_string(tree).encode('utf-8')
    temp_svg.write(svg_bytes)
    temp_svg.close()
    return temp_svg


def tree_to_file(tree, filename="output.svg"):
    """turn SVG tree into a tempfile"""
    svg_file = open(filename, "w")
    svg_bytes = svg_string(tree)
    svg_file.write(svg_bytes)
    svg_file.close()


def path_string_to_element(path_string, style=""):
    """Create SVG Element from path string"""
    if style == "":
        style = "fill:none;stroke:#231f20;stroke-miterlimit:10;stroke-width:0.25px"
    svg_element = ET.Element('path', attrib={'d': path_string, 'style': style})
    return svg_element
