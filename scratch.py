# scratch.py

"""scratch app for figuring things out"""

# from laser_svg_parser import parse_svgfile
import svgpathtools as SVGPT
# from laser_svg_utils import path_string_to_element, element_to_tree, tree_to_file
from laser_path_utils import separate_closed_paths, paths_to_loops, combine_paths
from laser_assistant import make_blank_model
from laser_clipper import point_inside_loop
from laser_svg_parser import model_to_svg_file


def svg_to_model(filename):
    """converts svg file to design model"""
    combined_path = svg_to_combined_paths(filename)
    closed_paths, _ = separate_closed_paths([combined_path])
    model = paths_to_faces(closed_paths)
    return model


def svg_to_combined_paths(filename):
    """converts svg file to a single combined path"""

    # original_style = "fill:#000000;fill-opacity:0.5;stroke:#ff0000;" + \
    #     f"stroke-linejoin:round;stroke-width:1.00px"
    paths, _ = SVGPT.svg2paths(filename)
    # svgdata = parse_svgfile(filename)
    combined_path = SVGPT.concatpaths(paths)

    return combined_path.d()


def paths_to_faces(paths):
    """takes a list of paths and returns model with faces"""
    model = make_blank_model()
    perims, cuts = separate_perims_from_cuts(paths)
    print(perims)
    print(cuts)
    for index, perim in enumerate(perims):
        model['tree'][f"face{index+1}"] = {
            "Perimeter": {'paths': [perim]}, "Cuts": {'paths': []}}
        for cut in cuts:
            if is_inside(cut, perim):
                model['tree'][f"face{index+1}"]['Cuts']['paths'].append(cut)
                # cuts.remove(cut)

    return model


def separate_perims_from_cuts(paths):
    """take a list of paths and returns two lists of paths faces and cuts."""
    perims = []
    cuts = []
    for path in paths:
        inside = False
        for other_path in paths:
            if other_path is not path:
                if is_inside(path, other_path):
                    inside = True
        if inside:
            cuts.append(path)
        else:
            perims.append(path)
    return perims, cuts


def is_inside(path, other_path):
    """checks if path is inside other_path and returns true or false"""
    loop = paths_to_loops([path])[0]
    other_loop = paths_to_loops([other_path])[0]
    for point in loop:
        if point_inside_loop(point, other_loop) == 1:
            return True
    return False


# def divide_pathstring_parts(pathstring):
#     """breaks single path string into substrings at each 'M' returning a list of path strings"""
#     substring = pathstring.strip()
#     paths = []
#     while 'M' in substring[1:]:
#         m_index = substring.find('M', 1)
#         if m_index > -1:
#             subpath = substring[0:m_index].strip()
#             paths.append(subpath)
#             substring = substring[m_index:].strip()

#     paths.append(substring)
#     return paths


# def get_discrete_paths(paths):
#     """takes a list of paths and breaks it down into discrete continuous paths"""
#     discrete_paths = []
#     for path in paths:
#         discrete_paths += divide_pathstring_parts(path)
#     return discrete_paths


# def split_closed_open_paths(paths):
#     """takes a list of paths and returns a tuple of closed, open paths"""
#     closed_paths = []
#     open_paths = []
#     for path in paths:
#         parsed_path = SVGPT.parse_path(path)
#         if parsed_path.isclosed():
#             closed_paths.append(path)
#         else:
#             open_paths.append(path)
#     return closed_paths, open_paths


# def pair_paths(paths):
#     """a single iteration attempts to find pairs of paths that share an endpoint,
#     and combine them into single paths. """
#     # return paired_paths + unpaired_paths
#     return paths


# def connect_paths(paths):
#     """checks for common path endpoints in a list of path strings,
#     and returns tuple of closed, open path string lists."""
#     # connected_paths = []

#     return paths

# def separate_closed_paths(paths):
#     """takes a list of path strings
#     breaks non continuous paths and
#     joins connecting paths together
#     to return a list of closed paths """
#     discrete_paths = []
#     closed_paths = []
#     open_paths = []
#     dead_ends = []
#     for path in paths:
#         discrete_paths += divide_pathstring_parts(path)
#     for path in discrete_paths:
#         parsed_path = SVGPT.parse_path(path)
#         if parsed_path.isclosed():
#             closed_paths.append(path)
#         else:
#             open_paths.append(parsed_path)
#     while open_paths:
#         path = open_paths.pop()
#         print(path)
#         new_path = None
#         for other_path in open_paths:
#             if path.end == other_path.start:
#                 new_path = path.d() + " " + other_path.d().replace('M', 'L')
#                 open_paths.remove(other_path)
#                 break
#             elif path.start == other_path.end:
#                 new_path = other_path.d() + " " + path.d().replace('M', 'L')
#                 open_paths.remove(other_path)
#                 break
#             elif path.end == other_path.end:
#                 new_path = path.d() + " " + other_path.reversed().d().replace('M', 'L')
#                 open_paths.remove(other_path)
#                 break
#             elif path.start == other_path.start:
#                 new_path = path.reversed().d() + " " + other_path.d().replace('M', 'L')
#                 open_paths.remove(other_path)
#                 break
#         if new_path is not None:
#             parsed_new_path = SVGPT.parse_path(new_path)
#             if parsed_new_path.isclosed():
#                 closed_paths.append(new_path)
#             else:
#                 open_paths.append(parsed_new_path)
#             print(new_path)
#         else:
#             dead_ends.append(path.d())
#     open_paths = dead_ends
#     return closed_paths, open_paths
if __name__ == "__main__":

    # do_more_stuff()
    # PATHSTRING1 = "M 0, 0 L 1, 0 M0, 0 L0, 1"
    # PATHSTRING2 = " M0, 1 L 1, 0"
    # PATHSTRING3 = "  M3,3L4,3L4,4L3,4Z"
    # PATHSTRING4 = "M5,5 L5,6 L6,6 M5,5 L6,5 L6,6"
    # PATHSTRING5 = "M7,7 L 8,8"
    # PATHS = [PATHSTRING1, PATHSTRING2, PATHSTRING3, PATHSTRING4, PATHSTRING5]
    # CP, OP = separate_closed_paths(PATHS)
    # print(CP)
    # print(OP)
    FILENAME = "input-samples/test8-01.svg"
    MODEL = svg_to_model(FILENAME)
    print(MODEL)
    model_to_svg_file(MODEL)
