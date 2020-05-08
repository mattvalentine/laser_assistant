# laser_assistant.py
"""A tool to generate joints for laser cutting"""

# import numpy as np


# def get_length(point1, point2):
#     """calculates the length of a segment √x²+y²"""
#     length = ((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)**0.5
#     return length


# def get_rotation_angle(point1, point2):
#     """returns the clockwise angle between a vector defined by 2 points and the x axis"""
#     # translating into complex vector = x + yj (j is the complex number)
#     vector = point2[0] - point1[0] + (point2[1] - point1[1])*1j

#     angle = np.angle(vector, deg=True)

#     return angle


# def points_from_line(line):
#     """generates points from line"""
#     point1 = [float(line.attrib["x1"]), float(line.attrib["y1"])]
#     point2 = [float(line.attrib["x2"]), float(line.attrib["y2"])]
#     return(point1, point2)

def make_blank_model():
    """Make a valid blank model"""
    model = {'tree': {}, 'attrib': {}}
    return model


def get_perimeters(faces):
    """returns a list of perimeter paths for all faces"""
    perimeters = []
    for shapes in faces.values():
        paths = shapes['Perimeter']['paths']
        for path in paths:
            perimeters.append(path)
    return perimeters


def get_cuts(faces):
    """returns a list of cut paths for all faces"""
    cuts = []
    for shapes in faces.values():
        paths = shapes['Cuts']['paths']
        for path in paths:
            cuts.append(path)
    return cuts


def get_length(joint):
    """returns the length of a joint"""
    return 100


def get_joint_path(joint, parameters):
    """Generates Joint from parameters"""
    length = get_length(joint)
    return []


def process_joint(joint, parameters, perimeters):
    """Generates, translates and rotates joint path into place"""
    joint_path = get_joint_path(joint, parameters)
    # placed_path
    return []


def process_joints(joints, parameters, perimeters):
    """returns a list of joint cut paths for all joints"""
    processed_joints = []
    # TODO: process joints with SVG Path Tools
    for joint in joints:
        for edge in ['A', 'B']:
            placed_path = process_joint(edge, parameters, perimeters)
            processed_joints.append(placed_path)

    return processed_joints


def subtract_geometry(perimeters, cuts):
    """cuts out joints and cuts from faces"""
    # TODO: process subtraction with clipper
    return perimeters+cuts


def get_geometry(tree, parameters):
    """returns paths of original and target geometry"""
    perimeters = get_perimeters(tree['Faces'])
    cuts = get_cuts(tree['Faces'])
    joints = process_joints(tree['Joints'], parameters, perimeters)
    original_geometry = subtract_geometry(perimeters, cuts)
    target_geometry = subtract_geometry(original_geometry, joints)
    return (original_geometry, target_geometry)


def process_design(design_model, parameters):
    """process design and parameters to produce output"""

    print("processing design... not really ", parameters)

    output_model = make_blank_model()
    output_model['attrib'] = design_model['attrib']

    original, target = get_geometry(design_model['tree'], parameters)

    output_model['tree']['Original'] = {'paths': original}
    output_model['tree']['Target'] = {'paths': target}

    # output_model['tree']['Original']['paths'] = perimeter_paths + cut_paths

    return output_model


if __name__ == "__main__":
    from laser_cmd_parser import laser_parser
    from svg_parser import parse_svgfile, model_to_svg_file

    IN_FILE, OUT_FILE, PARAMETERS = laser_parser()
    DESIGN = parse_svgfile(IN_FILE)
    OUTPUT = process_design(DESIGN, PARAMETERS)
    print(OUTPUT)
    model_to_svg_file(OUTPUT, filename=OUT_FILE)
