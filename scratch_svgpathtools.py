# scratch_svgpathtools.py
"""Experiments with SVGPathTools library for laser cutting applications"""

import tempfile
import xml.etree.ElementTree as ET
import svgpathtools as SVGPT
# it's imporatant to clone and install the repo manually. The pip/pypi version is outdated


# Namespace for svg formatting
NS = {'svg': 'http://www.w3.org/2000/svg'}

def get_viewbox(tree):
    """returns viewbox attribute of svg tree"""
    root = tree.getroot()
    viewbox = root.attrib["viewBox"]
    return viewbox

def new_svg_tree(viewbox):
    """create a new svg element tree"""
    new_root = ET.Element('svg')
    new_root.attrib["viewBox"] = viewbox
    new_root.attrib["xmlns"] = "http://www.w3.org/2000/svg"
    new_tree = ET.ElementTree(new_root)
    return new_tree

def svg_string(tree):
    """convert svg element tree object to a string without namespace junk"""
    root = tree.getroot()
    output_string = ET.tostring(root).decode("utf-8")
    output_string = output_string.replace('xmlns:svg="http://www.w3.org/2000/svg" ', "")
    output_string = output_string.replace("svg:", "")
    return output_string

def element_to_tree(element, viewbox):
    """SVG element + viewbox = new SVG tree with just that element"""
    tree = new_svg_tree(viewbox)
    root = tree.getroot()
    root.append(element)
    return tree

def tree_to_tempfile(tree):
    """turn SVG tree into a tempfile"""
    temp_svg = tempfile.NamedTemporaryFile(suffix=".svg")
    svg_bytes = svg_string(tree).encode('utf-8')
    temp_svg.write(svg_bytes)
    return temp_svg

def tempfile_to_paths(temp_svg):
    """open temp SVG file and return a path"""
    temp_svg.seek(0)
    paths, attributes = SVGPT.svg2paths(temp_svg.name)
    temp_svg.close()
    return (paths, attributes)

def tree_to_paths(tree):
    """turns an svg tree into a path"""
    temp_svg = tree_to_tempfile(tree)
    paths, attrib = tempfile_to_paths(temp_svg)
    return(paths, attrib)

def parse_svg_tree(svg_root, viewbox):
    """Recursive SVG parser"""
    svg_data = {}
    for item in svg_root:
        if item.tag == "{http://www.w3.org/2000/svg}g":
            if 'data-name' in item.attrib:
                svg_data[item.attrib['data-name']] = parse_svg_tree(item, viewbox)
            else:    
                svg_data[item.attrib['id']] = parse_svg_tree(item, viewbox)
        else:
            tree = element_to_tree(item, viewbox)
            svg_data['paths'], svg_data['attrib'] = tree_to_paths(tree)
    return svg_data

def parse_svgfile(filename):
    """Read joints and shapes from formatted SVG file."""
    tree = ET.parse(filename)
    viewbox = get_viewbox(tree)
    return parse_svg_tree(tree.getroot(), viewbox)

if __name__ == "__main__":
    FILENAME = "input-samples/test6-01.svg"
    THING = parse_svgfile(FILENAME)
    print(THING)
