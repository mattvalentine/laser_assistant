# laser_assistant.py
"""A tool to generate joints for laser cutting"""

import xml.etree.ElementTree as ET
import argparse
import os
import numpy as np

from box_joint_generator import make_box_joint_a, make_box_joint_b

# Namespace for svg formatting
NS = {'svg': 'http://www.w3.org/2000/svg'}

def run_parser():
    """Parses arguements and returns constants."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename")
    parser.add_argument("--thickness")
    parser.add_argument("--segments")

    parser.parse_args()

    args = parser.parse_args()

    if args.filename:
        filename = args.filename
    else:
        filename = 'input-samples/test1-01.svg'
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        exit()


    if args.thickness:
        thickness = float(args.thickness)
    else:
        thickness = 10
    if thickness <= 0:
        print(f"Invalid thickness: {thickness}")
        exit()

    if args.segments:
        segments = int(args.segments)
    else:
        segments = 5
    if segments < 3:
        print(f"Invalid segment quantity (Must be at least 3 segments): {segments}")
        exit()

    return(filename, thickness, segments)

def get_length(point1, point2):
    """calculates the length of a segment √x²+y²"""
    length = ((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)**0.5
    return length

def get_rotation_angle(point1, point2):
    """returns the clockwise angle between a vector defined by 2 points and the x axis"""
    # translating into complex vector = x + yj (j is the complex number)
    vector = point2[0] - point1[0] + (point2[1] - point1[1])*1j

    angle = np.angle(vector, deg=True)

    return angle

def points_from_line(line):
    """generates points from line"""
    point1 = [float(line.attrib["x1"]), float(line.attrib["y1"])]
    point2 = [float(line.attrib["x2"]), float(line.attrib["y2"])]
    return(point1, point2)

# TODO: change segments to more general type specific parameters
def generate_edge(line, thickness, segments, joint_a):
    """generates the joint edges"""
    point1, point2 = points_from_line(line)
    length = get_length(point1, point2)
    angle = get_rotation_angle(point1, point2)

    # TODO: implement logic for different joint types

    # uses external joint generator to create horizontal edge
    # (easy drop in replacement with other joint types)
    if joint_a:
        edge = make_box_joint_a(length, segments, thickness)
    else:
        edge = make_box_joint_b(length, segments, thickness)

    # places edge by rotating and moving the generated joint
    for seg in edge.findall('line'):
        rotate = f"rotate({angle},{point1[0]},{point1[1]})"
        translate = f"translate({point1[0]},{point1[1]})"
        seg.attrib["transform"] = rotate + " " + translate
        seg.set('updated', 'yes')

    return edge



def parse_svg(filename):
    """Read joints and shapes from formatted SVG file."""

    tree = ET.parse(filename)
    root = tree.getroot()

    # dictionaries for Joints and Shapes
    joints = {}
    shapes = {}

    # viewbox / artboard dimenstions
    viewbox = root.attrib["viewBox"]

    for layer in tree.findall('svg:g', NS):
        layer_name = layer.attrib['id']
        if layer_name.find("Joint") == 0:
            joints[layer_name] = []
            for line in layer.findall('svg:line', NS):
                joints[layer_name].append(line)
        if layer_name.find("Shape") == 0:
            shapes[layer_name] = []
            for line in layer.findall('svg:line', NS):
                shapes[layer_name].append(line)
    return(joints, shapes, viewbox)

def process_joints(joints, shapes, viewbox, thickness, segments):
    """Iterate through joints and modify shapes."""

    # create basic structure of output SVG
    new_root = ET.Element('svg')
    new_root.attrib["viewBox"] = viewbox
    new_root.attrib["xmlns"] = "http://www.w3.org/2000/svg"
    new_tree = ET.ElementTree(new_root)

    # make an output layer
    output = ET.SubElement(new_root, 'g')
    output.attrib['id'] = "Output"

    for index in shapes:
        shape = shapes[index]
        for line in shape:
            ET.SubElement(output, 'line', line.attrib)
    for index in joints:
        joint = joints[index]
        joint_a = True # joint A vs B
        for line in joint:
            edge = generate_edge(line, thickness, segments, joint_a)
            for seg in edge.findall('line'):
                output.append(seg)
            joint_a = not joint_a

    return new_tree

if __name__ == "__main__":
    FILENAME, THICKNESS, SEGMENTS = run_parser()
    (JOINTS, SHAPES, VIEWBOX) = parse_svg(FILENAME)
    OUTPUT_SVG = process_joints(JOINTS, SHAPES, VIEWBOX, THICKNESS, SEGMENTS)
    OUTPUT_SVG.write('output.svg')
    # os.system("open output.svg")
    