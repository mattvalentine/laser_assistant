# laser_assistant.py
"""A tool to generate joints for laser cutting"""

from laser_path_utils import (get_length, get_start, get_angle,
                              move_path, rotate_path,
                              get_overlapping, get_not_overlapping,
                              paths_to_loops, loops_to_paths,
                              separate_closed_paths, is_inside,
                              path_to_segments)
from laser_clipper import get_difference, get_offset_loop
import svgpathtools as SVGPT
from laser_svg_parser import separate_perims_from_cuts, parse_svgfile, model_to_svg_file
from joint_generators import FlatJoint, BoxJoint, TslotJoint


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
        f"stroke-linejoin:round;stroke-width:0px;display:None"

    for face, shapes in tree.items():
        if face.startswith('face'):
            perimeters = []
            perimeter_paths = shapes['Perimeter']['paths']
            for path in perimeter_paths:
                perimeters.append(path)
            cuts = []
            cut_paths = shapes['Cuts']['paths']
            if cut_paths != []:
                for path in cut_paths:
                    cuts.append(path)
                tree[face]['Original'] = {
                    'paths': subtract_geometry(perimeters, cuts),
                    'style': original_style}
            else:
                tree[face]['Original'] = {
                    'paths': perimeters,
                    'style': original_style}
    return tree


def get_processed(tree, parameters):
    """returns paths of original and target geometry"""
    processed_style = "fill:#00ff00;fill-opacity:0.1;stroke:#00ff00;" + \
        f"stroke-linejoin:round;stroke-width:0.25px"

    for face, shapes in tree.items():
        if face.startswith('face'):
            original = shapes['Original']['paths']
            joints = []
            if 'Joints' in shapes:
                for joint, edge in shapes['Joints'].items():
                    if joint.startswith('J'):
                        # print(joint)
                        processed_edge = process_edge(
                            joint[-1], edge, parameters)
                        joints.append(processed_edge)

                tree[face]['Processed'] = {
                    'paths': subtract_geometry(original, joints),
                    'style': processed_style}
            else:
                tree[face]['Processed'] = {
                    'paths': original,
                    'style': processed_style}
    return tree


def get_kerf(paths, kerf_size):
    """calculate kerf compensated path"""
    loops = paths_to_loops(paths)
    kerf_loops = get_offset_loop(loops, kerf_size / 2)
    kerf_paths = loops_to_paths(kerf_loops)
    return kerf_paths


def get_single_kerf(tree, parameters):
    """doesn't worry about inside vs outside"""
    kerf_size = parameters['kerf']
    kerf_style = f"fill:none;stroke:#ff0000;stroke-linejoin:round;" + \
        f"stroke-width:0.5px;stroke-linecap:round;stroke-opacity:0.5"
    for face, shapes in tree.items():
        if face.startswith('face'):
            original = shapes['Processed']['paths']
            kerf_path = get_kerf(original, kerf_size)
            tree[face]['Kerf'] = {
                'paths': kerf_path,
                'style': kerf_style}
    return tree


def get_outside_kerf(tree, parameters):
    """calculate kerf compensated path for visible surfaces"""
    slow_kerf_size = parameters['slow_kerf']
    visible_style = f"fill:none;stroke:#ff0000;stroke-linejoin:round;" + \
        f"stroke-width:{slow_kerf_size}px;stroke-linecap:round;stroke-opacity:0.5"

    for face, shapes in tree.items():
        if face.startswith('Face'):
            original = shapes['Original']['paths']
            processed = shapes['Processed']['paths']
            original_kerf = get_kerf(original, parameters['slow_kerf'])
            processed_kerf = get_kerf(processed, parameters['slow_kerf'])
            outside_kerf = get_overlapping(processed_kerf, original_kerf)
            # outside_kerf = intersect_paths(processed_kerf, original_kerf)
            tree[face]['Visible'] = {
                'paths': outside_kerf,
                'style': visible_style}
    return tree


def get_inside_kerf(tree, parameters):
    """calculate kerf compensated path for non-visible surfaces"""
    fast_kerf_size = parameters['fast_kerf']
    inside_style = f"fill:none;stroke:#0000ff;stroke-linejoin:round;" + \
        f"stroke-width:{fast_kerf_size}px;stroke-linecap:round;stroke-opacity:0.5"

    for face, shapes in tree.items():
        if face.startswith('Face'):
            original = shapes['Original']['paths']
            processed = shapes['Processed']['paths']
            original_kerf = get_kerf(original, parameters['fast_kerf'])
            processed_kerf = get_kerf(processed, parameters['fast_kerf'])
            # inside_kerf = subtract_paths(processed_kerf, original_kerf)
            inside_kerf = get_not_overlapping(processed_kerf, original_kerf)
            tree[face]['Hidden'] = {
                'paths': inside_kerf,
                'style': inside_style}
    return tree


def process_design(design_model, parameters):
    """process design and parameters to produce output"""
    design_model['tree'] = get_original(design_model['tree'])
    design_model['tree'] = get_processed(design_model['tree'], parameters)
    design_model['tree'] = get_outside_kerf(design_model['tree'], parameters)
    design_model['tree'] = get_inside_kerf(design_model['tree'], parameters)
    return design_model


def process_web_design(design_model, parameters):
    """process simple kerf offset"""
    kerf = parameters['kerf']
    # thickness = parameters['thickness']

    segments = 5
    joint_type = 'box'
    if joint_type == 'box':
        generator = BoxJoint
    elif joint_type == 'tslot':
        generator = TslotJoint
    else:
        generator = FlatJoint

    tsize = 'M2.5'
    bolt_length = 20.0
    clearance = 1.5
    bolts_per_side = segments

    parameters['segments'] = segments
    parameters['fast_kerf'] = kerf*1.2
    parameters['slow_kerf'] = kerf
    parameters['type'] = joint_type
    parameters['generator'] = generator
    parameters['tsize'] = tsize
    parameters['bolt_length'] = bolt_length
    parameters['clearance'] = clearance
    parameters['x_clearance'] = clearance
    parameters['y_clearance'] = clearance
    parameters['bolts_per_side'] = bolts_per_side

    design_model['tree'] = get_original(design_model['tree'])
    design_model = add_joints(design_model)
    design_model['tree'] = get_processed(design_model['tree'], parameters)
    design_model['tree'] = get_single_kerf(design_model['tree'], parameters)
    return design_model


def svg_to_model(filename):
    """converts svg file to design model"""
    svg_data = parse_svgfile(filename)
    combined_path = svg_to_combined_paths(filename)
    closed_paths, open_paths = separate_closed_paths([combined_path])
    model = paths_to_faces(closed_paths)
    model['attrib'] = svg_data['attrib']
    if open_paths != []:
        model['tree']['Open Paths'] = {'paths': open_paths}
    model['joints'] = {}
    model['edge_data'] = get_edges(model)
    return model


def get_edges(model):
    """separates edges into individual segments"""
    edge_data = {}
    edge_data['viewBox'] = model['attrib']['viewBox']
    edge_data['edges'] = []
    edge_count = 0
    tree = model['tree']
    for face, shapes in tree.items():
        if face.startswith('face'):
            perimeter = shapes['Perimeter']['paths'][0]
            segments = path_to_segments(perimeter)
            for segment in segments:
                edge = {}
                edge['d'] = segment
                edge['face'] = face
                edge_count = edge_count + 1
                edge['edge'] = edge_count
                edge_data['edges'].append(edge)
    return edge_data


def add_joints(model):
    """adds joints to tree"""
    tree = model['tree']
    joints = model['joints']
    for joint in joints:
        new_edge = {"paths": [joints[joint]['path']]}
        if 'Joints' not in tree[joints[joint]['face']]:
            tree[joints[joint]['face']]['Joints'] = {}
        tree[joints[joint]['face']]['Joints'][joint] = new_edge
    model['tree'] = tree
    return model


def svg_to_combined_paths(filename):
    """converts svg file to a single combined path"""
    paths, _ = SVGPT.svg2paths(filename)
    combined_path = SVGPT.concatpaths(paths)
    return combined_path.d()


def paths_to_faces(paths):
    """takes a list of paths and returns model with faces"""
    model = make_blank_model()
    perims, cuts = separate_perims_from_cuts(paths)

    for index, perim in enumerate(perims):
        model['tree'][f"face{index+1}"] = {
            "Perimeter": {'paths': [perim]}, "Cuts": {'paths': []}}
        for cut in cuts:
            if is_inside(cut, perim):
                model['tree'][f"face{index+1}"]['Cuts']['paths'].append(cut)

    return model


if __name__ == "__main__":
    # from laser_cmd_parser import parse_command
    # from laser_svg_parser import parse_svgfile, model_to_svg_file, separate_perims_from_cuts

    # IN_FILE, OUT_FILE, PARAMETERS = parse_command()
    # DESIGN = parse_svgfile(IN_FILE)
    # OUTPUT = process_design(DESIGN, PARAMETERS)
    # model_to_svg_file(OUTPUT, filename=OUT_FILE)

    # FILENAME = "input-samples/test8-01.svg"
    # FILENAME = "input-samples/test9-01.svg"
    FILENAME = "input-samples/100_x_100_x_345_drawer_alt.svg"
    MODEL = svg_to_model(FILENAME)
    print(MODEL)
    model_to_svg_file(MODEL)
