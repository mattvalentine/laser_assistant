# scratch_svgpathtools.py
"""Experiments with SVGPathTools library for laser cutting applications"""

import xml.etree.ElementTree as ET
from svgpathtools import Path, Line, QuadraticBezier, CubicBezier, Arc, svg2paths
# it's imporatant to clone and install the repo manually. The pip/pypi version is outdated

# Namespace for svg formatting
NS = {'svg': 'http://www.w3.org/2000/svg'}

def parse_svg(filename):
    """Read joints and shapes from formatted SVG file."""

    tree = ET.parse(filename)
    root = tree.getroot()

    # dictionaries for Joints and Shapes
    joints = {}
    faces = {}

    # viewbox / artboard dimenstions
    viewbox = root.attrib["viewBox"]
    print(viewbox)

    for layer in tree.findall('svg:g', NS):
        layer_name = layer.attrib['id']
        # print(layer_name)

        if layer_name == "Joints":
            for joint in layer.findall('svg:g', NS):
                joint_name = joint.attrib['id']
                # print(joint_name)
                joints[joint_name] = {}
                for edge in joint.findall('svg:g', NS):
                    edge_name = edge.attrib['id']
                    # print(edge_name)
                    joints[joint_name][edge_name] = ET.tostring(edge[0])
                    # print(ET.tostring(joints[joint_name][edge_name]))
            print(joints)

        if layer_name == "Faces":
            for face in layer.findall('svg:g', NS):
                face_name = face.attrib['id']
                # print(face_name)
                faces[face_name] = []
                for shape in face:
                    faces[face_name].append(ET.tostring(shape))
                    # print(ET.tostring(shape))


            print(faces)
    return(joints, faces, viewbox)

if __name__ == "__main__":
    FILENAME = "input-samples/test5-01.svg"
    # parse_svg(FILENAME)
    PATHS = svg2paths(FILENAME)

    for path in PATHS[0]:
        print(path)
    