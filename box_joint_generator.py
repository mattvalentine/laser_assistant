# box_joint_generator.py
"""A tool to make a box joint for laser cutting"""
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

def make_box_joint_a(length, segments, thickness):
    """generates a box joint"""

    joint = make_blank_svg(length, thickness)
    root = joint.getroot()

    # starting at the top
    last_point = [0, -thickness]

    for seg in range(segments):
        # make a segment
        next_point = [last_point[0]+length/segments, last_point[1]]
        new_segment = make_segment(last_point, next_point)
        root.append(new_segment)
        last_point = next_point

        # traverse to/from edge by thickness
        if seg+1 < segments:
            if seg%2 == 0:
                next_point = [last_point[0], last_point[1] + thickness]
            else:
                next_point = [last_point[0], last_point[1] - thickness]
            new_segment = make_segment(last_point, next_point)
            root.append(new_segment)
            last_point = next_point

    return joint

def make_box_joint_b(length, segments, thickness):
    """generates the opposite box joint"""

    joint = make_blank_svg(length, thickness)
    root = joint.getroot()

    # starts at the bottom instead of at the edge
    last_point = [0, 0]

    for seg in range(segments):
        # make a segment
        next_point = [last_point[0]+length/segments, last_point[1]]
        new_segment = make_segment(last_point, next_point)
        root.append(new_segment)

        # traverse to/from edge by thickness
        last_point = next_point
        if seg+1 < segments:
            if seg%2 == 1:
                next_point = [last_point[0], last_point[1] - thickness]
            else:
                next_point = [last_point[0], last_point[1] + thickness]
            new_segment = make_segment(last_point, next_point)
            root.append(new_segment)
            last_point = next_point

    return joint

if __name__ == "__main__":
    THICKNESS = 3.0
    LENGTH = 100.0
    SEGMENTS = 5

    NEWJOINTA = make_box_joint_a(LENGTH, SEGMENTS, THICKNESS)
    NEWJOINTB = make_box_joint_b(LENGTH, SEGMENTS, THICKNESS)

    NEWJOINTA.write('jointA.svg')
    NEWJOINTB.write('jointB.svg')
