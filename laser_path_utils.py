# laser_path_utils.py
"""Utility functions for working with paths for laser cutting"""

import svgpathtools as SVGPT
# it's imporatant to clone and install the repo manually. The pip/pypi version is outdated

from laser_svg_utils import tree_to_tempfile


def tempfile_to_paths(temp_svg):
    """open temp SVG file and return a path"""
    temp_svg.seek(0)
    paths, attributes = SVGPT.svg2paths(temp_svg.name)
    temp_svg.close()
    return (paths, attributes)


def tree_to_paths(tree):
    """turns an svg tree into paths list"""
    temp_svg = tree_to_tempfile(tree)
    paths, _ = tempfile_to_paths(temp_svg)
    svg_paths = []
    for path in paths:
        svg_paths.append(path.d())
    return svg_paths


def paths_to_points(paths):
    """"Convert a list of paths to a tupple of tupples of points"""
    point_loop_list = []
    for path_string in paths:
        point_loop_list.append(path_string_to_points(path_string))
    return tuple(point_loop_list)


def path_string_to_points(path_string):
    """Convert path string into a tupple of points"""
    path = SVGPT.parse_path(path_string)
    points = []
    for segment in path:
        segment_points = segment_to_points(segment)
        for point in segment_points:
            if points == [] or point != points[-1]:
                points.append(point)
    return tuple(points)


def segment_to_points(segment):
    """Converts a path segment into a tupple of points"""
    points = tuple([])
    if isinstance(segment, SVGPT.path.Line):  # pylint: disable=maybe-no-member
        points = points_from_line(segment)
    else:
        points = points_from_curve(segment)
    return points


def points_from_line(line):
    """returns endpoints of line"""
    points_list = []
    points_list.append(get_segment_point(line, 0))
    points_list.append(get_segment_point(line, 1))
    return tuple(points_list)


def points_from_curve(curve, samples=20):
    """returns poins along a curve"""
    points_list = []
    for location in range(samples + 1):
        point_on_curve = get_segment_point(curve, location)
        points_list.append(point_on_curve)
    return tuple(points_list)


def get_segment_point(segment, location):
    """gets point on segment at a location (between 0 and 1) returning cartesian tupple (x,y)"""
    complex_point = segment.point(location)
    cartesian_point = (complex_point.real, complex_point.imag)
    return cartesian_point


def loops_to_paths(loops):
    """turns a tupple of point loops into a list of path strings"""
    paths = []
    for loop in loops:
        path = points_to_path(loop)
        paths.append(path)
    return paths


def points_to_path(points):
    """turn a series of points into a path"""
    first = True
    data = "M "
    for point in points:
        if not first:
            data += " L "
        data += f"{point[0]},{point[1]}"
        first = False
    return data


if __name__ == "__main__":
    TEST_PATH = "M 150.0,10.0 L 250.0,10.0 L 250.0,110.0 L 150.0,110.0 L 150.0,10.0"
    POINTS = path_string_to_points(TEST_PATH)
    print(TEST_PATH)
    print(POINTS)
    print(points_to_path(POINTS))
    print()
    LOOPS = (((150.0, 10.0), (250.0, 10.0), (250.0, 110.0),
              (150.0, 110.0), (150.0, 10.0)),
             ((350.0, 70.0), (450.0, 70.0), (450.0, 170.0),
              (350.0, 170.0), (350.0, 70.0)))
    print(LOOPS)
    print(loops_to_paths(LOOPS))
