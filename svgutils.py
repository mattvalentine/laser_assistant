# box_joint_generator.py
"""Utility functions for working with SVGs"""
import xml.etree.ElementTree as ET


def make_blank_svg(width, height):
    """makes a blank svg with a viewbox matching the parameters"""
    new_root = ET.Element("svg")
    new_root.attrib["xmlns"] = "http://www.w3.org/2000/svg"
    new_root.attrib["viewBox"] = f"0 0 {width} {height}"
    new_tree = ET.ElementTree(new_root)
    return new_tree

def make_segment(point1, point2):
    """generates an svg line from two points"""
    segment = ET.Element("line")
    segment.attrib["style"] = "fill:none;stroke:#00a651;stroke-miterlimit:10;stroke-width:0.25px"
    segment.attrib["x1"] = f"{point1[0]}"
    segment.attrib["y1"] = f"{point1[1]}"
    segment.attrib["x2"] = f"{point2[0]}"
    segment.attrib["y2"] = f"{point2[1]}"
    return segment
