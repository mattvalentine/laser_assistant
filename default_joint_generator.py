# tslot_joint_generator.py
"""A template to make a generic joint for laser cutting"""

from svgutils import make_blank_svg, make_segment

def make_joint_a(joint_parameters):
    """generates a T-slot joint"""

    length = joint_parameters['length']
    thickness = joint_parameters['thickness']

    joint = make_blank_svg(length, thickness)
    root = joint.getroot()

    last_point = [0, 0]
    next_point = [length, 0]
    new_segment = make_segment(last_point, next_point)
    root.append(new_segment)

    return joint


def make_joint_b(joint_parameters):
    """generates the opposite T-slot joint"""

    length = joint_parameters['length']
    thickness = joint_parameters['thickness']

    joint = make_blank_svg(length, thickness)
    root = joint.getroot()

    last_point = [0, 0]
    next_point = [length, 0]
    new_segment = make_segment(last_point, next_point)
    root.append(new_segment)

    return joint

if __name__ == "__main__":
    JOINT_PARAMETERS = {}
    THICKNESS = 3.0
    LENGTH = 100.0
    SEGMENTS = 5
    JOINT_PARAMETERS['thickness'] = THICKNESS
    JOINT_PARAMETERS['length'] = LENGTH
    JOINT_PARAMETERS['segments'] = SEGMENTS

    NEWJOINTA = make_joint_a(JOINT_PARAMETERS)
    NEWJOINTB = make_joint_b(JOINT_PARAMETERS)

    NEWJOINTA.write('jointA.svg')
    NEWJOINTB.write('jointB.svg')
