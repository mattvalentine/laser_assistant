# joint_generators.py
"""A tool to make a joint for laser cutting"""

from laser_svg_utils import path_string_to_element, element_to_tree, tree_to_file
# import svgpathtools as SVGPT


def joint_to_file(joint_path, viewbox, style="", filename="joint.svg"):
    """converts joint path string to svg file"""
    if style == "":
        style = "fill:#231f20;stroke:#231f20;stroke-miterlimit:10;stroke-width:0.25px"
    joint_element = path_string_to_element(joint_path, style)
    joint_tree = element_to_tree(joint_element, viewbox)
    tree_to_file(joint_tree, filename=filename)


# TODO: Add T-slot class

class FlatJoint:
    """Generators for Flat Joints"""

    def make_a(self, parameters):
        """Generate A half of the Joint"""
        length = parameters['length']

        data = f"M 0 0 L {length} 0"

        return data

    def make_b(self, parameters):
        """Generate B half of the Joint"""
        length = parameters['length']
        thickness = parameters['thickness']
        y_clearance = parameters['y_clearance']

        pt_y = thickness + y_clearance

        data = f"M 0 0 L 0 {pt_y}"
        data += f" L {length} {pt_y} L {length} 0"

        return data


class BoxJoint:
    """Generators for Box Joints"""

    def make_a(self, parameters):
        """Generate A half of the Joint"""
        segments = parameters['segments']
        length = parameters['length']
        thickness = parameters['thickness']
        x_clearance = parameters['x_clearance']
        y_clearance = parameters['y_clearance']

        pt_y = thickness + y_clearance
        inside = False

        data = f"M 0 0"

        for step in range(segments-1):
            pt_x = (step+1) * (length/segments)
            if inside:
                data += f" L {pt_x+x_clearance/4} {pt_y} L {pt_x+x_clearance/4} 0"
            else:
                data += f" L {pt_x-x_clearance/4} 0 L {pt_x-x_clearance/4} {pt_y}"
            inside = not inside

        data += f" L {length} 0"

        return data

    def make_b(self, parameters):
        """Generate B half of the Joint"""
        segments = parameters['segments']
        length = parameters['length']
        thickness = parameters['thickness']
        x_clearance = parameters['x_clearance']
        y_clearance = parameters['y_clearance']

        pt_y = thickness + y_clearance
        inside = True

        data = f"M 0 0 L 0 {pt_y}"

        for step in range(segments-1):
            pt_x = (step+1) * (length/segments)
            if inside:
                data += f" L {pt_x+x_clearance/4} {pt_y} L {pt_x+x_clearance/4} 0"
            else:
                data += f" L {pt_x-x_clearance/4} 0 L {pt_x-x_clearance/4} {pt_y}"
            inside = not inside

        data += f" L {length} {pt_y} L {length} 0"

        return data


if __name__ == "__main__":
    # import xml.etree.ElementTree as ET
    # from laser_svg_utils import path_string_to_element, element_to_tree

    JOINT_PARAMETERS = {}
    THICKNESS = 3.0
    LENGTH = 100.0
    SEGMENTS = 5
    X_CLEARANCE = 0.1
    Y_CLEARANCE = 0.25
    JOINT_PARAMETERS['thickness'] = THICKNESS
    JOINT_PARAMETERS['length'] = LENGTH
    JOINT_PARAMETERS['segments'] = SEGMENTS
    JOINT_PARAMETERS['x_clearance'] = X_CLEARANCE
    JOINT_PARAMETERS['y_clearance'] = Y_CLEARANCE

    # JOINT = FlatJoint()
    JOINT = BoxJoint()

    JOINT_A = JOINT.make_a(JOINT_PARAMETERS)
    JOINT_B = JOINT.make_b(JOINT_PARAMETERS)

    joint_to_file(JOINT_A, "0 0 100 100", filename="jointA.svg")
    joint_to_file(JOINT_B, "0 0 100 100", filename="jointB.svg")
