# laser_assistant.py
"""A tool to generate joints for laser cutting"""
# Generator for laser cut joints

import xml.etree.ElementTree as ET
import argparse
import os

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
        filename = 'input-samples/test1.svg'

    if args.thickness:
        thickness = float(args.thickness)
    else:
        thickness = 10

    if args.segments:
        segments = int(args.segments)
    else:
        segments = 5
    return(filename, thickness, segments)

# TODO: parse more arguements:
# input file
# material thickness
# joint type
# joint parameters: different for different joint types...
# for box joint: number of segments
# output name?

# TODO: make function - get line equation
# TODO: make function - get line range
# TODO: make line overlap function

# TODO: make joint generator more generalized

def generate_edge(line, inside, thickness, segments):
    """Take an edge from a joint (line+direction) as input and generate line segments for output."""
    # for the moment this is hard coded to left and right as 1 and 2
    edge = []
    # temporary hard coded vertical joint only
    length = abs(float(line.attrib['y1']) - float(line.attrib['y2']))
    segment_length = length / segments
    rightx = float(line.attrib['x1'])
    leftx = float(line.attrib['x1']) - thickness

    segment_attrib = line.attrib

    top_y = max(float(line.attrib['y1']), float(line.attrib['y2']))

    segment_inside = inside
    segment_y = top_y

    # TODO: break these segment generators down into subfunctions
    for i in range(segments):
        new_segment = ET.Element('{http://www.w3.org/2000/svg}line', segment_attrib)
        if segment_inside:
            new_segment.attrib['x1'] = f"{leftx:.5f}"
            new_segment.attrib['y1'] = f"{segment_y:.5f}"
            new_segment.attrib['x2'] = f"{leftx:.5f}"
            segment_y = segment_y - segment_length
            new_segment.attrib['y2'] = f"{segment_y:.5f}"
            edge.append(new_segment)
            if i+1 != segments:
                new_segment = ET.Element('{http://www.w3.org/2000/svg}line', segment_attrib)
                new_segment.attrib['x1'] = f"{leftx:.5f}"
                new_segment.attrib['y1'] = f"{segment_y:.5f}"
                new_segment.attrib['x2'] = f"{rightx:.5f}"
                new_segment.attrib['y2'] = f"{segment_y:.5f}"
                edge.append(new_segment)
        else:
            new_segment.attrib['x1'] = f"{rightx:.5f}"
            new_segment.attrib['y1'] = f"{segment_y:.5f}"
            new_segment.attrib['x2'] = f"{rightx:.5f}"
            segment_y = segment_y - segment_length
            new_segment.attrib['y2'] = f"{segment_y:.5f}"
            edge.append(new_segment)
            if i+1 != segments:
                new_segment = ET.Element('{http://www.w3.org/2000/svg}line', segment_attrib)
                new_segment.attrib['x1'] = f"{rightx:.5f}"
                new_segment.attrib['y1'] = f"{segment_y:.5f}"
                new_segment.attrib['x2'] = f"{leftx:.5f}"
                new_segment.attrib['y2'] = f"{segment_y:.5f}"
                edge.append(new_segment)
        segment_inside = not segment_inside

    return edge


def parse_svg(filename):
    """Read joints and shapes from formatted SVG file."""

    tree = ET.parse(filename)
    root = tree.getroot()

    # dictionaries for Joints and Shapes
    joints = {}
    shapes = {}
    # viewbox / artboard attributes
    viewbox = root.attrib

    for layer in tree.findall('{http://www.w3.org/2000/svg}g'):
        layer_name = layer.attrib['id']
        if layer_name.find("Joint") == 0:
            joints[layer_name] = []
            for line in layer.findall('{http://www.w3.org/2000/svg}line'):
                joints[layer_name].append(line)
        if layer_name.find("Shape") == 0:
            shapes[layer_name] = []
            for line in layer.findall('{http://www.w3.org/2000/svg}line'):
                shapes[layer_name].append(line)
    return(joints, shapes, viewbox)

def process_joints(joints, shapes, viewbox, thickness, segments):
    """Iterate through joints and modify shapes."""

    # create basic structure of output SVG
    new_root = ET.Element('{http://www.w3.org/2000/svg}svg', viewbox)
    new_tree = ET.ElementTree(new_root)

    # make an output layer
    output = ET.SubElement(new_root, '{http://www.w3.org/2000/svg}g')
    output.attrib['id'] = "Output"

    for index in shapes:
        shape = shapes[index]
        for line in shape:
            ET.SubElement(output, 'line', line.attrib)
    for index in joints:
        joint = joints[index]
        inside = False
        for line in joint:
            edge = generate_edge(line, inside, thickness, segments)
            for segment in edge:
                ET.SubElement(output, 'line', segment.attrib)
    return new_tree

if __name__ == "__main__":
    FILENAME, THICKNESS, SEGMENTS = run_parser()
    (JOINTS, SHAPES, VIEWBOX) = parse_svg(FILENAME)
    OUTPUT_SVG = process_joints(JOINTS, SHAPES, VIEWBOX, THICKNESS, SEGMENTS)
    OUTPUT_SVG.write('output.svg')
    os.system("open output.svg")
    