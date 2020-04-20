# box_joint_generator.py
"""A tool to make a box joint for laser cutting"""

from svgutils import make_blank_svg, make_segment

def make_box_joint_a(joint_parameters):
    """generates a box joint"""

    length = joint_parameters['length']
    segments = joint_parameters['segments']
    thickness = joint_parameters['thickness']

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

def make_box_joint_b(joint_parameters):
    """generates the opposite box joint"""

    length = joint_parameters['length']
    segments = joint_parameters['segments']
    thickness = joint_parameters['thickness']

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
    JOINT_PARAMETERS = {}
    THICKNESS = 3.0
    LENGTH = 100.0
    SEGMENTS = 5
    JOINT_PARAMETERS['thickness'] = THICKNESS
    JOINT_PARAMETERS['length'] = LENGTH
    JOINT_PARAMETERS['segments'] = SEGMENTS

    NEWJOINTA = make_box_joint_a(JOINT_PARAMETERS)
    NEWJOINTB = make_box_joint_b(JOINT_PARAMETERS)

    NEWJOINTA.write('jointA.svg')
    NEWJOINTB.write('jointB.svg')
