# laser_assistant.py
"""A tool to generate joints for laser cutting"""

from laser_path_utils import (get_length, get_start, get_angle,
                              move_path, rotate_path,
                              subtract_paths, intersect_paths,
                              paths_to_loops, loops_to_paths)
from laser_clipper import get_difference, get_offset_loop


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


def place_new_edge_path(new_edge_path, old_edge_path):
    """moves and rotates new path to line up with old path"""
    # assert get_angle(new_edge_path) == 0

    start_point = get_start(old_edge_path)
    moved_path = move_path(new_edge_path, start_point)

    rotation_angle = get_angle(old_edge_path)
    rotated_path = rotate_path(moved_path, rotation_angle, start_point)

    return rotated_path


def process_edge(a_or_b, edge, parameters):
    """Generates, translates and rotates joint path into place"""
    assert 'paths' in edge
    assert len(edge['paths']) == 1

    old_edge_path = edge['paths'][0]
    parameters['length'] = get_length(old_edge_path)
    generator = parameters['generator']()

    new_edge_path = generator.make(a_or_b, parameters)
    placed_path = place_new_edge_path(new_edge_path, old_edge_path)

    return placed_path


def process_joints(joints, parameters):
    """returns a list of joint cut paths for all joints"""
    processed_joints = []
    for joint in joints.values():
        for edge in ['A', 'B']:
            placed_path = process_edge(edge, joint[edge], parameters)
            processed_joints.append(placed_path)
    return processed_joints


def subtract_geometry(perimeters, cuts):
    """subtracts cuts from faces"""
    perimeters_loops = paths_to_loops(perimeters)
    cuts_loops = paths_to_loops(cuts)
    differnce_loops = get_difference(perimeters_loops, cuts_loops)
    differnce = loops_to_paths(differnce_loops)
    # differnce = loops_to_paths(cuts_loops)
    return differnce


def get_geometry(tree, parameters):
    """returns paths of original and target geometry"""
    perimeters = get_perimeters(tree['Faces'])
    cuts = get_cuts(tree['Faces'])
    joints = process_joints(tree['Joints'], parameters)
    cut_geometry = subtract_geometry(perimeters, cuts)
    processed_geometry = subtract_geometry(cut_geometry, joints)
    return (perimeters, processed_geometry)


def get_kerf(paths, kerf_size):
    """calculate kerf compensated path"""
    loops = paths_to_loops(paths)
    kerf_loops = get_offset_loop(loops, kerf_size / 2)
    kerf_paths = loops_to_paths(kerf_loops)
    return kerf_paths


def get_outside_kerf(original, processed, parameters):
    """calculate kerf compensated path for visible surfaces"""
    original_kerf = get_kerf(original, parameters['slow_kerf'])
    processed_kerf = get_kerf(processed, parameters['slow_kerf'])
    outside_kerf = intersect_paths(processed_kerf, original_kerf)
    return outside_kerf


def get_inside_kerf(original, processed, parameters):
    """calculate kerf compensated path for non-visible surfaces"""
    original_kerf = get_kerf(original, parameters['fast_kerf'])
    processed_kerf = get_kerf(processed, parameters['fast_kerf'])
    inside_kerf = subtract_paths(processed_kerf, original_kerf)
    return inside_kerf


def process_design(design_model, parameters):
    """process design and parameters to produce output"""

    original, processed = get_geometry(design_model['tree'], parameters)

    outside_kerf = get_outside_kerf(original, processed, parameters)
    inside_kerf = get_inside_kerf(original, processed, parameters)

    output_model = make_blank_model()
    output_model['attrib'] = design_model['attrib']

    output_model['tree']['Original'] = {'paths': original}
    original_style = "fill:none;stroke:#000000;stroke-miterlimit:10;stroke-width:0.25px"
    output_model['tree']['Original']['style'] = original_style

    output_model['tree']['Processed'] = {'paths': processed}
    processed_style = "fill:none;stroke:#00ff00;stroke-miterlimit:10;stroke-width:0.25px"
    output_model['tree']['Processed']['style'] = processed_style

    output_model['tree']['Visible'] = {'paths': outside_kerf}
    visible_style = "fill:none;stroke:#ff0000;stroke-miterlimit:10;stroke-width:0.25px"
    output_model['tree']['Visible']['style'] = visible_style

    output_model['tree']['Hidden'] = {'paths': inside_kerf}
    inside_style = "fill:none;stroke:#0000ff;stroke-miterlimit:10;stroke-width:0.25px"
    output_model['tree']['Hidden']['style'] = inside_style

    return output_model


if __name__ == "__main__":
    from laser_cmd_parser import laser_parser
    from laser_svg_parser import parse_svgfile, model_to_svg_file

    IN_FILE, OUT_FILE, PARAMETERS = laser_parser()
    DESIGN = parse_svgfile(IN_FILE)
    OUTPUT = process_design(DESIGN, PARAMETERS)
    model_to_svg_file(OUTPUT, filename=OUT_FILE)
