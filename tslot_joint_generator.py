# tslot_joint_generator.py
"""A tool to make a T-slot joint for laser cutting"""

# TODO: Convert to new class in joint_generators.py

from svgutils import make_blank_svg, make_segment

NUT_BOLT_SIZES = {'M2.5': {'nut_width': 5.0,
                           'nut_height': 2.0, 'bolt_diameter': 2.5}}


def make_tslot_sequence(nut_bolt_parameters):
    """generates a T shaped cut out for nut and bolt"""
    print(nut_bolt_parameters)

    tsize = nut_bolt_parameters['tsize']
    bolt_length = nut_bolt_parameters['bolt_length']
    clearance = nut_bolt_parameters['clearance']
    thickness = nut_bolt_parameters['thickness']

    nut_bolt_sizes = NUT_BOLT_SIZES[tsize]
    nut_height = nut_bolt_sizes['nut_height']
    nut_width = nut_bolt_sizes['nut_width']
    bolt_diameter = nut_bolt_sizes['bolt_diameter']

    x_a = bolt_diameter/2.0 + clearance
    x_b = nut_width/2.0 + clearance

    y_a = -bolt_length + thickness + 2.0 * nut_height
    y_b = -bolt_length + thickness + nut_height - 2.0 * clearance
    y_c = -bolt_length + thickness - 2.0 * clearance

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

    print(sequence)

    return sequence


def make_notch_sequence(nut_bolt_parameters):
    """generates a T shaped cut out for nut and bolt"""
    print(nut_bolt_parameters)

    tsize = nut_bolt_parameters['tsize']
    clearance = nut_bolt_parameters['clearance']
    thickness = nut_bolt_parameters['thickness']

    nut_bolt_sizes = NUT_BOLT_SIZES[tsize]
    bolt_diameter = nut_bolt_sizes['bolt_diameter']

    x_a = bolt_diameter/2.0 + clearance

    y_a = thickness/2.0 + bolt_diameter/2.0 * clearance

    sequence = []

    sequence.append([-x_a, 0])
    sequence.append([-x_a, y_a])
    sequence.append([x_a, y_a])
    sequence.append([x_a, 0])

    print(sequence)

    return sequence


def make_tslot_joint_a(joint_parameters):
    """generates a T-slot joint"""

    length = joint_parameters['length']
    thickness = joint_parameters['thickness']
    bolts_per_side = joint_parameters['bolts_per_side']

    tsize = joint_parameters['tsize']
    bolt_length = joint_parameters['bolt_length']
    clearance = joint_parameters['clearance']
    thickness = joint_parameters['thickness']

    joint = make_blank_svg(length, thickness)
    root = joint.getroot()

    nut_bolt_parameters = {}
    nut_bolt_parameters['tsize'] = tsize
    nut_bolt_parameters['bolt_length'] = bolt_length
    nut_bolt_parameters['clearance'] = clearance
    nut_bolt_parameters['thickness'] = thickness
    tslot_sequence = make_tslot_sequence(nut_bolt_parameters)

    slot_interval = length / (bolts_per_side + 1)

    last_point = [0, 0]
    bolt_location = [0, 0]
    for _ in range(bolts_per_side):
        bolt_location = [bolt_location[0] + slot_interval, 0]
        for step in tslot_sequence:
            next_point = [bolt_location[0] +
                          step[0], bolt_location[1] + step[1]]
            new_segment = make_segment(last_point, next_point)
            root.append(new_segment)
            last_point = next_point
    next_point = [bolt_location[0] + slot_interval, 0]
    new_segment = make_segment(last_point, next_point)
    root.append(new_segment)
    last_point = next_point

    return joint


def make_tslot_joint_b(joint_parameters):
    """generates the opposite T-slot joint"""
    length = joint_parameters['length']
    thickness = joint_parameters['thickness']
    bolts_per_side = joint_parameters['bolts_per_side']

    tsize = joint_parameters['tsize']
    # bolt_length = joint_parameters['bolt_length']
    clearance = joint_parameters['clearance']
    thickness = joint_parameters['thickness']

    joint = make_blank_svg(length, thickness)
    root = joint.getroot()

    nut_bolt_parameters = {}
    nut_bolt_parameters['tsize'] = tsize
    # nut_bolt_parameters['bolt_length'] = bolt_length
    nut_bolt_parameters['clearance'] = clearance
    nut_bolt_parameters['thickness'] = thickness
    tslot_sequence = make_notch_sequence(nut_bolt_parameters)

    slot_interval = length / (bolts_per_side + 1)

    last_point = [0, 0]
    bolt_location = [0, 0]
    for _ in range(bolts_per_side):
        bolt_location = [bolt_location[0] + slot_interval, 0]
        for step in tslot_sequence:
            next_point = [bolt_location[0] +
                          step[0], bolt_location[1] + step[1]]
            new_segment = make_segment(last_point, next_point)
            root.append(new_segment)
            last_point = next_point
    next_point = [bolt_location[0] + slot_interval, 0]
    new_segment = make_segment(last_point, next_point)
    root.append(new_segment)
    last_point = next_point

    return joint


if __name__ == "__main__":
    JOINT_PARAMETERS = {}
    THICKNESS = 3.0
    LENGTH = 100.0
    SEGMENTS = 5
    JOINT_PARAMETERS['thickness'] = THICKNESS
    JOINT_PARAMETERS['length'] = LENGTH
    JOINT_PARAMETERS['segments'] = SEGMENTS

    NEWJOINTA = make_tslot_joint_a(JOINT_PARAMETERS)
    NEWJOINTB = make_tslot_joint_b(JOINT_PARAMETERS)

    NEWJOINTA.write('jointA.svg')
    NEWJOINTB.write('jointB.svg')
