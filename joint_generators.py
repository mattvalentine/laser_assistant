# joint_generators.py
"""A tool to make a joint for laser cutting"""

from laser_svg_utils import path_string_to_element, element_to_tree, tree_to_file
# import svgpathtools as SVGPT


def joint_to_file(joint_path, viewbox, style="", filename="joint.svg"):
    """converts joint path string to svg file"""
    if style == "":
        style = "fill:#231f20;stroke:#231f20;stroke-miterlimit:10;stroke-width:0.25px"
    joint_element = path_string_to_element(joint_path, style)
    attrib = {'viewBox': viewbox}
    joint_tree = element_to_tree(joint_element, attrib)
    tree_to_file(joint_tree, filename=filename)


class Joint:
    """Parent Generators for Joints"""

    def make(self, a_or_b, parameters):
        """Shortcut to run make_a or make_b by checking string a_or_b to match 'A' or 'B"""
        assert (a_or_b == 'A' or a_or_b == 'B')

        if a_or_b == 'A':
            return self.make_a(parameters)
        else:
            return self.make_b(parameters)

    def make_a(self, parameters):
        """Generate A half of the Joint"""
        length = parameters['length']
        data = f"M 0 0 L {length} 0 Z"
        return data

    def make_b(self, parameters):
        """Generate B half of the Joint"""
        length = parameters['length']
        data = f"M 0 0 L {length} 0 Z"
        return data


class FlatJoint(Joint):
    """Generators for Flat Joints"""

    def make_a(self, parameters):
        """Generate A half of the Joint"""
        length = parameters['length']

        data = f"M 0 0 L {length} 0 Z"

        return data

    def make_b(self, parameters):
        """Generate B half of the Joint"""
        length = parameters['length']
        thickness = parameters['thickness']
        y_clearance = parameters['y_clearance']

        pt_y = thickness + y_clearance

        data = f"M 0 0 L 0 {pt_y}"
        data += f" L {length} {pt_y} L {length} 0"
        data += " Z"

        return data


class BoxJoint(Joint):
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

        data += f" L {length} 0 Z"

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

        data += f" L {length} {pt_y} L {length} 0 Z"

        return data


class TslotJoint(Joint):
    """Generators for T-slot Joints"""
    NUT_BOLT_SIZES = {'M2.5': {'nut_width': 5.0,
                               'nut_height': 2.0, 'bolt_diameter': 2.5}}

    def make_tslot_sequence(self, nut_bolt_parameters):
        """generates a T shaped cut out for nut and bolt"""

        tsize = nut_bolt_parameters['tsize']
        bolt_length = nut_bolt_parameters['bolt_length']
        clearance = nut_bolt_parameters['clearance']
        thickness = nut_bolt_parameters['thickness']

        nut_bolt_sizes = self.NUT_BOLT_SIZES[tsize]
        nut_height = nut_bolt_sizes['nut_height']
        nut_width = nut_bolt_sizes['nut_width']
        bolt_diameter = nut_bolt_sizes['bolt_diameter']

        x_a = bolt_diameter/2.0 + clearance
        x_b = nut_width/2.0 + clearance

        # y_a = -bolt_length + thickness + 2.0 * nut_height
        # y_b = -bolt_length + thickness + nut_height - 2.0 * clearance
        # y_c = -bolt_length + thickness - 2.0 * clearance
        y_a = bolt_length - thickness - 2.0 * nut_height
        y_b = bolt_length - thickness - nut_height + 2.0 * clearance
        y_c = bolt_length - thickness + 2.0 * clearance

        sequence = []

        sequence.append([-x_a, 0])
        sequence.append([-x_a, y_a])
        sequence.append([-x_b, y_a])
        sequence.append([-x_b, y_b])
        sequence.append([-x_a, y_b])
        sequence.append([-x_a, y_c])
        sequence.append([x_a, y_c])
        sequence.append([x_a, y_b])
        sequence.append([x_b, y_b])
        sequence.append([x_b, y_a])
        sequence.append([x_a, y_a])
        sequence.append([x_a, 0])

        return sequence

    def make_notch_sequence(self, nut_bolt_parameters):
        """generates a T shaped cut out for nut and bolt"""

        tsize = nut_bolt_parameters['tsize']
        clearance = nut_bolt_parameters['clearance']
        thickness = nut_bolt_parameters['thickness']

        nut_bolt_sizes = self.NUT_BOLT_SIZES[tsize]
        bolt_diameter = nut_bolt_sizes['bolt_diameter']

        x_a = bolt_diameter/2.0 + clearance

        y_a = thickness/2.0 + bolt_diameter/2.0 * clearance

        sequence = []

        sequence.append([-x_a, 0])
        sequence.append([-x_a, y_a])
        sequence.append([x_a, y_a])
        sequence.append([x_a, 0])

        return sequence

    def make_a(self, parameters):
        """generates a T-slot joint"""

        length = parameters['length']
        thickness = parameters['thickness']
        bolts_per_side = parameters['bolts_per_side']

        tsize = parameters['tsize']
        bolt_length = parameters['bolt_length']
        clearance = parameters['clearance']
        thickness = parameters['thickness']

        nut_bolt_parameters = {}
        nut_bolt_parameters['tsize'] = tsize
        nut_bolt_parameters['bolt_length'] = bolt_length
        nut_bolt_parameters['clearance'] = clearance
        nut_bolt_parameters['thickness'] = thickness
        tslot_sequence = self.make_tslot_sequence(nut_bolt_parameters)

        slot_interval = length / (bolts_per_side + 1)
        data = "M 0,0"
        # last_point = [0, 0]
        bolt_location = [0, 0]
        for _ in range(bolts_per_side):
            bolt_location = [bolt_location[0] + slot_interval, 0]
            for step in tslot_sequence:
                next_point = [bolt_location[0] +
                              step[0], bolt_location[1] + step[1]]
                data += f" L {next_point[0]},{next_point[1]}"
                # last_point = next_point
        next_point = [bolt_location[0] + slot_interval, 0]
        data += f" L {next_point[0]},{next_point[1]} Z"

        return data

    def make_b(self, parameters):
        """generates a T-slot joint"""

        length = parameters['length']
        thickness = parameters['thickness']
        bolts_per_side = parameters['bolts_per_side']

        tsize = parameters['tsize']
        bolt_length = parameters['bolt_length']
        clearance = parameters['clearance']
        thickness = parameters['thickness']

        nut_bolt_parameters = {}
        nut_bolt_parameters['tsize'] = tsize
        nut_bolt_parameters['bolt_length'] = bolt_length
        nut_bolt_parameters['clearance'] = clearance
        nut_bolt_parameters['thickness'] = thickness
        tslot_sequence = self.make_notch_sequence(nut_bolt_parameters)

        slot_interval = length / (bolts_per_side + 1)
        data = "M 0,0"
        # last_point = [0, 0]
        bolt_location = [0, 0]
        for _ in range(bolts_per_side):
            bolt_location = [bolt_location[0] + slot_interval, 0]
            for step in tslot_sequence:
                next_point = [bolt_location[0] +
                              step[0], bolt_location[1] + step[1]]
                data += f" L {next_point[0]},{next_point[1]}"
                # last_point = next_point
        next_point = [bolt_location[0] + slot_interval, 0]
        data += f" L {next_point[0]},{next_point[1]} Z"

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

    JOINT_PARAMETERS['tsize'] = 'M2.5'
    JOINT_PARAMETERS['bolt_length'] = 20.0
    JOINT_PARAMETERS['clearance'] = 0.1
    JOINT_PARAMETERS['bolts_per_side'] = SEGMENTS

    # JOINT = FlatJoint()
    # JOINT = BoxJoint()
    JOINT = TslotJoint()

    JOINT_A = JOINT.make('A', JOINT_PARAMETERS)
    JOINT_B = JOINT.make('B', JOINT_PARAMETERS)

    joint_to_file(JOINT_A, "0 0 100 100", filename="jointA.svg")
    joint_to_file(JOINT_B, "0 0 100 100", filename="jointB.svg")
