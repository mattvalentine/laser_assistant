# laser_assistant.py
"""A tool to generate joints for laser cutting"""
import xml.etree.ElementTree as ET
import json

from laser_path_utils import (get_length, get_start, get_angle,
                              move_path, rotate_path,
                              get_overlapping, get_not_overlapping,
                              paths_to_loops, loops_to_paths,
                              separate_closed_paths, is_inside,
                              path_to_segments)
from laser_clipper import get_difference, get_offset_loop, get_union
import svgpathtools.svgpathtools as SVGPT
from laser_svg_parser import separate_perims_from_cuts, parse_svgfile, model_to_svg_file
# from joint_generators import FlatJoint, BoxJoint, TslotJoint


def make_blank_model(attrib=None):
    """Make a valid blank model"""
    if attrib is None:
        attrib = {}
    if "id" in attrib:
        del attrib['id']
    attrib['xmlns'] = "http://www.w3.org/2000/svg"

    model = {'tree': {}, 'attrib': attrib}
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


def combine_geometry(first, second):
    """combines two path lists"""
    first_loops = paths_to_loops(first)
    second_loops = paths_to_loops(second)
    combined_loops = get_union(first_loops, second_loops)
    combined = loops_to_paths(combined_loops)
    # differnce = loops_to_paths(cuts_loops)
    return combined

# def get_original(tree):
#     """returns paths of original and target geometry"""
#     original_style = "fill:#00ff00;fill-opacity:0.1;stroke:#000000;" + \
#         f"stroke-linejoin:round;stroke-width:0px"

#     for face, shapes in tree.items():
#         if face.startswith('face'):
#             perimeters = []
#             perimeter_paths = shapes['Perimeter']['paths']
#             for path in perimeter_paths:
#                 perimeters.append(path)
#             cuts = []
#             cut_paths = shapes['Cuts']['paths']
#             if cut_paths != []:
#                 for path in cut_paths:
#                     cuts.append(path)
#                 tree[face]['Original'] = {
#                     'paths': subtract_geometry(perimeters, cuts),
#                     'style': original_style}
#             else:
#                 tree[face]['Original'] = {
#                     'paths': perimeters,
#                     'style': original_style}
#     return tree


def get_original_tree(model):
    """returns paths (zero stroke with green fill) of original model"""
    tree = {}
    for face, shapes in model['tree'].items():
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
                tree[face] = {
                    'paths': subtract_geometry(perimeters, cuts)}
            else:
                tree[face] = {
                    'paths': perimeters}
    return tree


def process_joints(model, joints, parameters):
    """takes in model of paces and returns modified model with joints applied"""
    # print(joints)
    # print(parameters)
    for jointname, joint in joints.items():
        extensions = get_joint_adds(joint, model, parameters)
        # print(jointname, extensions)
        for face, extension in extensions.items():
            model['tree'][face]['paths'] = combine_geometry(
                model['tree'][face]['paths'], extension)

    for jointname, joint in joints.items():
        cuts = get_joint_cuts(joint, model, parameters)
        # print(jointname, cuts)
        for face, cut in cuts.items():
            model['tree'][face]['paths'] = subtract_geometry(
                model['tree'][face]['paths'], cut)
    return model


def get_box_joint_cuts(joint, model, parameters):
    """generator for box joints"""
    cuts = {}
    fits = {'Wood': {'Clearance': -0.05, 'Friction': 0.05, 'Press': 0.075},
            'Acrylic': {'Clearance': -0.1, 'Friction': 0.0, 'Press': 0.0}}
    patha = joint['edge_a']['d']
    pathb = joint['edge_b']['d']
    facea = joint['edge_a']['face']
    faceb = joint['edge_b']['face']
    lengtha = get_length(patha)
    lengthb = get_length(pathb)
    tabsize = joint['joint_parameters']['tabsize']
    tabspace = joint['joint_parameters']['tabspace']
    tabnum = joint['joint_parameters']['tabnum']
    thickness = parameters['thickness']
    fit = fits[parameters['material']][joint['joint_parameters']['fit']]
    print(fit+tabsize)
    sega = tabsize*tabnum + tabspace*(tabnum-1) - fit
    segb = tabsize*tabnum + tabspace*(tabnum-1) + fit
    offseta = (lengtha - sega) / 2.0
    offsetb = (lengthb - segb) / 2.0

    cuta = f""
    position = offseta
    for _ in range(tabnum):
        cuta += f"M {position} {0} " + \
                f"L {position} {thickness}" + \
                f"L {position + tabsize - fit} {thickness}" + \
                f"L {position + tabsize - fit} {0} Z "
        position = position + tabsize+tabspace

    cutb = f"M {0} {0} " + f"L {0} {thickness} " + \
           f"L {offsetb} {thickness} " + f"L {offsetb} {0} Z "
    position = offsetb
    print(offsetb)
    step = tabsize + tabspace
    for _ in range(tabnum - 1):
        cutb += f"M {position+tabsize+fit} {0} " + f"L {position+tabsize+fit} {thickness} " + \
                f"L {position+tabsize+tabspace} {thickness} " + \
                f"L {position+tabsize+tabspace} {0} Z "
        position = position + step
    position = position + tabsize
    cutb += f"M {position+fit} {0} " + f"L {position+fit} {thickness} " + \
            f"L {lengthb} {thickness} " + f"L {lengthb} {0} Z "

    cuts[facea] = [place_new_edge_path(cuta, patha)]
    cuts[faceb] = [place_new_edge_path(cutb, pathb)]

    return cuts


def get_interlock_joint_adds(joint, model, parameters):
    """generator for interlock joints"""
    adds = {}
    patha = joint['edge_a']['d']
    pathb = joint['edge_b']['d']
    facea = joint['edge_a']['face']
    faceb = joint['edge_b']['face']
    lengtha = get_length(patha)
    lengthb = get_length(pathb)
    thickness = parameters['thickness']

    adda = f"M {0} {0} "+f"L {0} {-thickness} " + \
        f"L {lengtha} {-thickness} "+f"L {lengtha} {0}"
    addb = f"M {0} {0} "+f"L {0} {-thickness} " + \
        f"L {lengthb} {-thickness} "+f"L {lengthb} {0}"

    adds[facea] = [place_new_edge_path(adda, patha)]
    adds[faceb] = [place_new_edge_path(addb, pathb)]

    return adds


def get_tabslot_joint_adds(joint, model, parameters):
    """generator for tabslot joints"""
    adds = {}
    patha = joint['edge_a']['d']
    pathb = joint['edge_b']['d']
    facea = joint['edge_a']['face']
    faceb = joint['edge_b']['face']
    lengtha = get_length(patha)
    lengthb = get_length(pathb)
    thickness = parameters['thickness']

    adda = f"M {0} {0} "+f"L {0} {-thickness} " + \
        f"L {lengtha} {-thickness} "+f"L {lengtha} {0}"
    # addb = f"M {0} {0} "+f"L {0} {-thickness} " + \
    #     f"L {lengthb} {-thickness} "+f"L {lengthb} {0}"

    adds[facea] = [place_new_edge_path(adda, patha)]
    # adds[faceb] = [place_new_edge_path(addb, pathb)]

    return adds


def get_bolt_joint_adds(joint, model, parameters):
    """generator for bolt joints"""
    adds = {}
    patha = joint['edge_a']['d']
    pathb = joint['edge_b']['d']
    facea = joint['edge_a']['face']
    faceb = joint['edge_b']['face']
    lengtha = get_length(patha)
    lengthb = get_length(pathb)
    thickness = parameters['thickness']

    adda = f"M {0} {0} "+f"L {0} {-thickness} " + \
        f"L {lengtha} {-thickness} "+f"L {lengtha} {0}"
    # addb = f"M {0} {0} "+f"L {0} {-thickness} " + \
    #     f"L {lengthb} {-thickness} "+f"L {lengthb} {0}"

    adds[facea] = [place_new_edge_path(adda, patha)]
    # adds[faceb] = [place_new_edge_path(addb, pathb)]

    return adds


def get_tabslot_joint_cuts(joint, model, parameters):
    """generator for tabslot joints"""
    cuts = {}
    fits = {'Wood': {'Clearance': -0.05, 'Friction': 0.05, 'Press': 0.1},
            'Acrylic': {'Clearance': -0.1, 'Friction': 0.0, 'Press': 0.0}}
    patha = joint['edge_a']['d']
    pathb = joint['edge_b']['d']
    facea = joint['edge_a']['face']
    faceb = joint['edge_b']['face']
    lengtha = get_length(patha)
    lengthb = get_length(pathb)
    tabsize = joint['joint_parameters']['tabsize']
    tabspace = joint['joint_parameters']['tabspace']
    tabnum = joint['joint_parameters']['tabnum']
    thickness = parameters['thickness']
    fit = fits[parameters['material']][joint['joint_parameters']['fit']]
    offseta = (lengtha - (tabsize * tabnum) - (tabspace * (tabnum - 1))) / 2
    offsetb = (lengthb - ((tabsize + fit) * tabnum) -
               ((tabspace - fit) * (tabnum - 1))) / 2

    cuta = f""
    position = 0
    step = offseta
    for _ in range(tabnum):
        position = position + step
        cuta += f"M {position} {0} " + \
                f"L {position} {thickness}" + \
                f"L {position + tabsize} {thickness}" + \
                f"L {position + tabsize} {0} Z "
        step = tabsize + tabspace

    cutb = f"M {0} {0} " + f"L {0} {thickness} " + \
           f"L {offsetb} {thickness} " + f"L {offsetb} {0} Z "
    position = offsetb
    step = tabsize + tabspace
    for _ in range(tabnum - 1):
        cutb += f"M {position+tabsize} {0} " + f"L {position+tabsize} {thickness} " + \
                f"L {position+tabsize+fit+tabspace} {thickness} " + \
                f"L {position+tabsize+fit+tabspace} {0} Z "
        position = position + step
    position = position + tabsize
    cutb += f"M {position} {0} " + f"L {position} {thickness} " + \
            f"L {lengthb} {thickness} " + f"L {lengthb} {0} Z "

    cuts[facea] = [place_new_edge_path(cuta, patha)]
    cuts[faceb] = [place_new_edge_path(cutb, pathb)]

    return cuts


def get_bolt_joint_cuts(joint, model, parameters):
    """generator for bolt joints"""
    cuts = {}

    NUT_BOLT_SIZES = {'M2': {'nut_width': 3.3,
                             'nut_height': 2.0,
                             'bolt_diameter': 2},
                      'M2.5': {'nut_width': 4.3,
                               'nut_height': 2.0,
                               'bolt_diameter': 2.5},
                      'M3': {'nut_width': 5.5,
                             'nut_height': 2.0,
                             'bolt_diameter': 3.0},
                      'M4': {'nut_width': 7.0,
                             'nut_height': 2.0,
                             'bolt_diameter': 4.0}}
    CLEARANCE = 0.1

    patha = joint['edge_a']['d']
    pathb = joint['edge_b']['d']
    facea = joint['edge_a']['face']
    faceb = joint['edge_b']['face']
    lengtha = get_length(patha)
    lengthb = get_length(pathb)
    thickness = parameters['thickness']

    bolt_size = joint['joint_parameters']['boltsize']
    bolt_space = joint['joint_parameters']['boltspace']
    bolt_num = joint['joint_parameters']['boltnum']
    bolt_length = joint['joint_parameters']['boltlength']

    nut_width = NUT_BOLT_SIZES[bolt_size]['nut_width'] + CLEARANCE
    nut_height = NUT_BOLT_SIZES[bolt_size]['nut_height'] + CLEARANCE
    bolt_diameter = NUT_BOLT_SIZES[bolt_size]['bolt_diameter'] + CLEARANCE

    segment_length = nut_width * 3
    combined_length = bolt_num * segment_length + \
        bolt_space * (bolt_num - 1)
    buffer_size_a = (lengtha - combined_length) / 2
    buffer_size_b = (lengthb - combined_length) / 2

    X_0 = 0
    X_1 = (nut_width - bolt_diameter) / 2
    X_2 = (nut_width + bolt_diameter) / 2
    X_3 = nut_width

    Y_0 = 0
    Y_1 = thickness
    Y_2 = bolt_length - (2*nut_height)
    Y_3 = bolt_length - nut_height
    Y_4 = bolt_length

    cuts[facea] = []
    # cuta = f""
    position = buffer_size_a
    for _ in range(bolt_num):
        cuta = f"M {position} {0} " + \
            f"L {position} {thickness} " + \
            f"L {position+nut_width} {thickness} " + \
            f"L {position+nut_width} {0} " + \
            f"L {position} {0} "
        cuts[facea].append(place_new_edge_path(cuta, patha))
        cuta = f"M {position+nut_width+X_1} {thickness/2} " + \
            f"A {bolt_diameter/2} {bolt_diameter/2} 0 0 1 " + \
            f"{position+nut_width+X_1 + bolt_diameter} {thickness/2} " + \
            f"M {position+nut_width+X_1 + bolt_diameter} {thickness/2} " + \
            f"A {bolt_diameter/2} {bolt_diameter/2} 0 0 1 " + \
            f"{position+nut_width+X_1} {thickness/2} "
        cuts[facea].append(place_new_edge_path(cuta, patha))
        cuta = f"M {position+2*nut_width} {0} " + \
            f"L {position+2*nut_width} {thickness} " + \
            f"L {position+nut_width+2*nut_width} {thickness} " + \
            f"L {position+nut_width+2*nut_width} {0} Z "
        cuts[facea].append(place_new_edge_path(cuta, patha))
        position = position + bolt_space + segment_length

    # cuta += f"M {position} {0} " + \
    #         f"L {position} {thickness} " + \
    #         f"L {position+nut_width} {thickness} " + \
    #         f"L {position+nut_width} {0} Z "
    # print(cuta)
    cuts[faceb] = []
    # cuta = f""
    cutb = f"M {0} {0} " + \
        f"L {0} {thickness} " + \
        f"L {buffer_size_b} {thickness} " + \
        f"L {buffer_size_b} {0} Z "
    cutb += f"M {lengthb} {0} " + \
        f"L {lengthb} {thickness} " + \
        f"L {lengthb - buffer_size_b} {thickness} " + \
        f"L {lengthb - buffer_size_b} {0} Z "
    cuts[faceb].append(place_new_edge_path(cutb, pathb))

    position = buffer_size_b
    for bolt in range(bolt_num):
        cutb = f"M {position+nut_width} {0} " + \
            f"L {position+nut_width} {thickness} " + \
            f"L {position+nut_width*2} {thickness} " + \
            f"L {position+nut_width*2} {0} Z "
        cuts[faceb].append(place_new_edge_path(cutb, pathb))
        if bolt < bolt_num:
            cutb = f"M {position+segment_length} {0} " + \
                f"L {position+segment_length} {thickness} " + \
                f"L {position+segment_length+bolt_space} {thickness} " + \
                f"L {position+segment_length+bolt_space} {0} Z "
            cuts[faceb].append(place_new_edge_path(cutb, pathb))
        position = position + bolt_space + segment_length

    position = buffer_size_b
    for bolt in range(bolt_num):
        cutb = f"M {position+nut_width+X_1} {Y_0} " + \
            f"L {position+nut_width+X_1} {Y_2} " + \
            f"L {position+nut_width+X_0} {Y_2} " + \
            f"L {position+nut_width+X_0} {Y_3} " + \
            f"L {position+nut_width+X_1} {Y_3} " + \
            f"L {position+nut_width+X_1} {Y_4} " + \
            f"L {position+nut_width+X_2} {Y_4} " + \
            f"L {position+nut_width+X_2} {Y_3} " + \
            f"L {position+nut_width+X_3} {Y_3} " + \
            f"L {position+nut_width+X_3} {Y_2} " + \
            f"L {position+nut_width+X_2} {Y_2} " + \
            f"L {position+nut_width+X_2} {Y_0} Z "
        cuts[faceb].append(place_new_edge_path(cutb, pathb))
        position = position + bolt_space + segment_length

    # cutb = f"M {lengt} {0} L {0} {thickness} L {buffer_size_b} {thickness} L {buffer_size_b} {0} Z"

    # cuts[facea] = [place_new_edge_path(cuta, patha)]
    # cuts[faceb] = [place_new_edge_path(cutb, pathb)]

    return cuts


def get_interlock_joint_cuts(joint, model, parameters):
    """generator for interlock joints"""
    cuts = {}
    fits = {'Wood': {'Clearance': 0, 'Friction': 1, 'Press': 2},
            'Acrylic': {'Clearance': 0, 'Friction': 0.1, 'Press': 0.2}}
    patha = joint['edge_a']['d']
    pathb = joint['edge_b']['d']
    facea = joint['edge_a']['face']
    faceb = joint['edge_b']['face']
    lengtha = get_length(patha)
    lengthb = get_length(pathb)
    joint_length = min(lengtha, lengthb)
    cut_length = joint_length / 2
    thickness = parameters['thickness']

    fit = fits[parameters['material']][joint['joint_parameters']['fit']]

    cuta = f""

    cuta += f"M {0} {0} " + \
            f"L {0} {thickness-fit}" + \
            f"L {cut_length} {thickness-fit}" + \
            f"L {cut_length} {0} Z "

    cutb = f"M {0} {0} " + \
           f"L {0} {thickness-fit}" + \
           f"L {cut_length} {thickness-fit}" + \
           f"L {cut_length} {0} Z "

    cuts[facea] = [place_new_edge_path(cuta, patha)]
    cuts[faceb] = [place_new_edge_path(cutb, pathb)]

    return cuts


def get_joint_adds(joint, model, parameters):
    """process a single joint"""
    jointtype = joint['joint_parameters']['joint_type']
    addfunc = {'Tab-and-Slot': get_tabslot_joint_adds,
               'Interlocking': get_interlock_joint_adds,
               'Bolt': get_bolt_joint_adds}
    adds = addfunc.get(jointtype, lambda j, m, c: {})(joint, model, parameters)
    return adds


def get_joint_cuts(joint, model, parameters):
    """process a single joint"""
    jointtype = joint['joint_parameters']['joint_type']
    cutfunc = {'Box': get_box_joint_cuts,
               'Tab-and-Slot': get_tabslot_joint_cuts,
               'Interlocking': get_interlock_joint_cuts,
               'Bolt': get_bolt_joint_cuts}
    cuts = cutfunc.get(jointtype, lambda j, m, c: {})(joint, model, parameters)
    return cuts


def kerf_offset(model, parameters):
    """Applies a kerf offset based upon material and laser parameters"""
    kerf_size = parameters['kerf']
    original_tree = model['tree']
    tree = {}
    for face, shapes in original_tree.items():
        if face.startswith('face'):
            original = shapes['paths']
            kerf_path = get_kerf(original, kerf_size)
            tree[face] = {
                'paths': kerf_path}

    return tree


def get_processed_model(model, parameters):
    """returns model containing paths of target geometry for each face"""

    output_model = make_blank_model(model['attrib'])
    # output_model['attrib'] = model['attrib']

    original_model = get_original_model(model)
    processed_model = process_joints(
        original_model, model['joints'], parameters)
    output_model['tree'] = kerf_offset(processed_model, parameters)

    return output_model


def get_kerf(paths, kerf_size):
    """calculate kerf compensated path using PyClipper"""
    # PyClipper understands loops not paths
    loops = paths_to_loops(paths)
    kerf_loops = get_offset_loop(loops, kerf_size)
    # change back into paths for output
    kerf_paths = loops_to_paths(kerf_loops)
    return kerf_paths


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


def process_web_outputsvg(design_model, parameters):
    """process joints and offset kerf"""
    # Processing:
    output_model = get_processed_model(design_model, parameters)
    # Styling:
    output_model['attrib']['style'] = f"fill:none;stroke:#ff0000;stroke-linejoin:round;" + \
        f"stroke-width:0.1px;stroke-linecap:round;stroke-opacity:0.5"

    return output_model


def get_original_model(input_model):
    """process simple kerf offset"""
    output_model = make_blank_model(input_model['attrib'])
    # output_model['attrib'] = input_model['attrib']
    output_model['attrib']['style'] = "fill:#00ff00;fill-opacity:0.25;stroke:none"
    output_model['tree'] = get_original_tree(input_model)
    return output_model


def svg_to_model(filename):
    """converts svg file to design model"""
    model = extract_embeded_model(filename)
    if model is None:
        model = model_from_raw_svg(filename)
    return model


def extract_embeded_model(filename):
    """extracts embeded model if there is one in metadata"""
    model = None
    tree = ET.parse(filename)
    root = tree.getroot()

    for metadata in root.findall('{http://www.w3.org/2000/svg}metadata'):
        lasermetadata = metadata.find(
            '{http://www.w3.org/2000/svg}laserassistant')
        if lasermetadata is not None:
            model = json.loads(lasermetadata.attrib['model'])
    return model


def model_from_raw_svg(filename):
    """creates a new model from a raw svg file without metadata"""
    svg_data = parse_svgfile(
        filename)

    combined_path = svg_to_combined_paths(filename)
    closed_paths, open_paths = separate_closed_paths([combined_path])
    model = paths_to_faces(closed_paths)
    model['attrib'] = svg_data['attrib']
    if open_paths != []:
        model['tree']['Open Paths'] = {'paths': open_paths}
    model['joints'] = {}
    model['edge_data'] = get_edges(model)
    model['joint_index'] = 1
    return model


def get_edges(model):
    """separates perimeter into individual segments"""
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
