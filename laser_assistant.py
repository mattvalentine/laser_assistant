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


# def process_joints(joints, parameters):
#     """returns a list of joint cut paths for all joints"""
#     processed_joints = []
#     for joint in joints.values():
#         for edge in ['A', 'B']:
#             placed_path = process_edge(edge, joint[edge], parameters)
#             processed_joints.append(placed_path)
#     return processed_joints


def subtract_geometry(perimeters, cuts):
    """subtracts cuts from faces"""
    perimeters_loops = paths_to_loops(perimeters)
    cuts_loops = paths_to_loops(cuts)
    differnce_loops = get_difference(perimeters_loops, cuts_loops)
    differnce = loops_to_paths(differnce_loops)
    # differnce = loops_to_paths(cuts_loops)
    return differnce


def get_original(tree):
    """returns paths of original and target geometry"""
    original_style = "fill:#000000;fill-opacity:0.1;stroke:#000000;" + \
        f"stroke-miterlimit:10;stroke-width:0.25px"

    for face, shapes in tree.items():
        if face.startswith('Face'):
            perimeters = []
            perimeter_paths = shapes['Perimeter']['paths']
            for path in perimeter_paths:
                perimeters.append(path)
            cuts = []
            cut_paths = shapes['Cuts']['paths']
            for path in cut_paths:
                cuts.append(path)
            tree[face]['Original'] = {
                'paths': subtract_geometry(perimeters, cuts),
                'style': original_style}
    return tree


def get_processed(tree, parameters):
    """returns paths of original and target geometry"""
    processed_style = "fill:#00ff00;fill-opacity:0.1;stroke:#00ff00;" + \
        f"stroke-miterlimit:10;stroke-width:0.25px"

    for face, shapes in tree.items():
        if face.startswith('Face'):
            original = shapes['Original']['paths']
            joints = []
            for joint, edge in shapes['Joints'].items():
                if joint.startswith('J'):
                    processed_edge = process_edge(joint[-1], edge, parameters)
                    joints.append(processed_edge)

            tree[face]['Processed'] = {
                'paths': subtract_geometry(original, joints),
                'style': processed_style}
    return tree


def get_kerf(paths, kerf_size):
    """calculate kerf compensated path"""
    loops = paths_to_loops(paths)
    kerf_loops = get_offset_loop(loops, kerf_size / 2)
    kerf_paths = loops_to_paths(kerf_loops)
    return kerf_paths


def get_outside_kerf(tree, parameters):
    """calculate kerf compensated path for visible surfaces"""
    slow_kerf_size = parameters['slow_kerf']
    visible_style = f"fill:none;stroke:#ff0000;stroke-miterlimit:10;" + \
        f"stroke-width:{slow_kerf_size}px;stroke-linecap:round;stroke-opacity:0.5"

    for face, shapes in tree.items():
        if face.startswith('Face'):
            original = shapes['Original']['paths']
            processed = shapes['Processed']['paths']
            original_kerf = get_kerf(original, parameters['slow_kerf'])
            processed_kerf = get_kerf(processed, parameters['slow_kerf'])
            outside_kerf = intersect_paths(processed_kerf, original_kerf)
            tree[face]['Visible'] = {
                'paths': outside_kerf,
                'style': visible_style}
    return tree


def get_inside_kerf(tree, parameters):
    """calculate kerf compensated path for non-visible surfaces"""
    fast_kerf_size = parameters['fast_kerf']
    inside_style = f"fill:none;stroke:#0000ff;stroke-miterlimit:10;" + \
        f"stroke-width:{fast_kerf_size}px;stroke-linecap:round;stroke-opacity:0.5"

    for face, shapes in tree.items():
        if face.startswith('Face'):
            original = shapes['Original']['paths']
            processed = shapes['Processed']['paths']
            original_kerf = get_kerf(original, parameters['fast_kerf'])
            processed_kerf = get_kerf(processed, parameters['fast_kerf'])
            outside_kerf = subtract_paths(processed_kerf, original_kerf)
            tree[face]['Hidden'] = {
                'paths': outside_kerf,
                'style': inside_style}
    return tree


def process_design(design_model, parameters):
    """process design and parameters to produce output"""
    design_model['tree'] = get_original(design_model['tree'])
    design_model['tree'] = get_processed(design_model['tree'], parameters)
    design_model['tree'] = get_outside_kerf(design_model['tree'], parameters)
    design_model['tree'] = get_inside_kerf(design_model['tree'], parameters)
    return design_model


if __name__ == "__main__":
    from laser_cmd_parser import parse_command
    from laser_svg_parser import parse_svgfile, model_to_svg_file

    import time

    START_TIME = time.time()

    IN_FILE, OUT_FILE, PARAMETERS = parse_command()
    DESIGN = parse_svgfile(IN_FILE)
    OUTPUT = process_design(DESIGN, PARAMETERS)
    model_to_svg_file(OUTPUT, filename=OUT_FILE)

    print(f"--- {(time.time() - START_TIME):.2f} seconds ---")
