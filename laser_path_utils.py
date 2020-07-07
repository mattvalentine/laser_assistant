# laser_path_utils.py
"""Utility functions for working with paths for laser cutting"""

import numpy as np

import svgpathtools as SVGPT
# it's imporatant to clone and install the repo manually. The pip/pypi version is outdated

from laser_svg_utils import tree_to_tempfile
from laser_clipper import point_on_loops


def tempfile_to_paths(temp_svg):
    """open temp SVG file and return a path"""
    # temp_svg.seek(0)
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


def paths_to_loops(paths):
    """"Convert a list of paths to a list of points"""
    point_loop_list = []
    for path_string in paths:
        point_loop_list.append(path_string_to_points(path_string))
    return point_loop_list


def combine_paths(paths, as_list=True):
    """combines path strings into a single string"""
    combined = ""
    first = True
    for path in paths:
        if not first:
            combined += " "
        combined += path
        first = False

    if as_list:
        return [combined]
    else:
        return combined


def path_string_to_points(path_string):
    """Convert path string into a list of points"""
    path = SVGPT.parse_path(path_string)
    points = []
    for segment in path:
        segment_points = subpath_to_points(segment)
        for point in segment_points:
            if points == [] or point != points[-1]:
                points.append(point)
    return points


def subpath_to_points(segment):
    """Converts a path segment into a list of points"""
    points = []
    if isinstance(segment, SVGPT.path.Line):  # pylint: disable=maybe-no-member
        points = points_from_line(segment)
    else:
        points = points_from_curve(segment)
    return points


def get_start(path_string):
    """returns start point (x, y) of a path string"""
    path = SVGPT.parse_path(path_string)
    start_xy = complex_to_xy(path.start)
    return start_xy


def points_from_line(line):
    """returns endpoints of line"""
    points_list = []
    start = line.point(0)
    end = line.point(1)
    points_list.append(complex_to_xy(start))
    points_list.append(complex_to_xy(end))
    return points_list


def points_from_curve(curve, samples=20):
    """returns poins along a curve"""
    points_list = []
    for location in range(samples + 1):
        point_on_curve = curve.point(location)
        points_list.append(complex_to_xy(point_on_curve))
    return points_list


def complex_to_xy(complex_point):
    """turns complex point (x+yj) into cartesian point [x,y]"""
    xy_point = [complex_point.real, complex_point.imag]
    return xy_point


def xy_to_complex(xy_point):
    """turns cartesian point [x,y] into complex point (x+yj)"""
    complex_point = xy_point[0] + xy_point[1] * 1j
    return complex_point


def loops_to_paths(loops):
    """turns a list of point loops into a list of path strings"""
    paths = []
    for loop in loops:
        path = points_to_path(loop)
        paths.append(path)
    return paths


def points_to_path(points, closed=True):
    """turn a series of points into a path"""
    first = True
    data = "M "
    for point in points:
        if not first:
            data += " L "
        data += f"{point[0]},{point[1]}"
        first = False
    if closed:
        data += " Z"
    return data


def move_path(path_string, xy_translation):
    """Takes a path string and xy_translation (x, y), and moves it x units over, and y units down"""
    path = SVGPT.parse_path(path_string)
    complex_translation = xy_to_complex(xy_translation)
    translated_path = path.translated(complex_translation)
    translated_string = translated_path.d()
    return translated_string


def get_angle(path_string):
    """measures the angle in degrees (CCW) from the path positive X axis (0,0), (0,1)"""
    path = SVGPT.parse_path(path_string)
    vector = path.point(1) - path.point(0)
    angle = np.angle(vector, deg=True)
    return angle


def rotate_path(path_string, angle_degrees, xy_point):
    """rotates a path string a given number of degrees (CCW) around point (x, y)"""
    path = SVGPT.parse_path(path_string)
    complex_point = xy_to_complex(xy_point)
    rotated_path = path.rotated(angle_degrees, origin=complex_point)
    rotated_string = rotated_path.d()
    return rotated_string


def get_length(path_string):
    """returns the length of a path string"""
    path = SVGPT.parse_path(path_string)
    return path.length()


def get_all_segments(loops):
    """returns all of the segments from all of the loops"""
    all_segments = []
    for loop in loops:
        loop_segments = get_loop_segments(loop)
        all_segments = all_segments + loop_segments
    return all_segments


def segments_overlap(first, second):
    """returns true if segments share more than a single point"""
    first_path_string = points_to_path(first, closed=False)
    second_path_string = points_to_path(second, closed=False)
    first_path = SVGPT.parse_path(first_path_string)[0]
    second_path = SVGPT.parse_path(second_path_string)[0]
    overlaps = []
    for point in first:
        complex_point = xy_to_complex(point)
        place_on_path = second_path.point_to_t(complex_point)
        if place_on_path is not None:
            if point not in overlaps:
                overlaps.append(point)
    for point in second:
        complex_point = xy_to_complex(point)
        place_on_path = first_path.point_to_t(complex_point)
        if place_on_path is not None:
            if point not in overlaps:
                overlaps.append(point)
    overlap = len(overlaps) >= 2
    return overlap


def get_loop_segments(loop):
    """returns a list of segments in a loop"""
    segments = []
    last_point = None
    for this_point in loop:
        if last_point is not None:
            new_segment = [last_point, this_point]
            segments.append(new_segment)
        last_point = this_point
    return segments


def segments_to_paths(segments):
    """converts list of segments into list of paths"""
    paths = []
    for segment in segments:
        new_path = points_to_path(segment, closed=False)
        paths.append(new_path)
    return paths


def get_not_overlapping(first, second):
    """returns the segments of the first path that do not overlap with the second."""
    output_paths = []

    first_loops = paths_to_loops(first)
    second_loops = paths_to_loops(second)

    for loop in first_loops:
        not_overlapping = ""
        segment_started = False
        last_point = loop[-1]
        for point in loop:
            if not point_on_loops(point, second_loops):
                if not segment_started:
                    not_overlapping += f" M {last_point[0]},{last_point[1]}"
                    segment_started = True
                if last_point != point:
                    not_overlapping += f" L {point[0]},{point[1]}"
            else:  # close the path
                if segment_started:
                    not_overlapping += f" L {point[0]},{point[1]}"
                    output_paths.append(not_overlapping)
                    segment_started = False
                    not_overlapping = ""
            last_point = point
        if segment_started:
            output_paths.append(not_overlapping)
    return output_paths


def get_overlapping(first, second):
    """returns the overlapping segments of the first and second path."""
    output_paths = []
    first_loops = paths_to_loops(first)
    second_loops = paths_to_loops(second)

    for loop in first_loops:
        overlapping = ""
        segment_started = False
        for point in loop:
            if point_on_loops(point, second_loops):
                if not segment_started:
                    overlapping += f" M {point[0]},{point[1]}"
                    segment_started = True
                else:
                    overlapping += f" L {point[0]},{point[1]}"
            else:  # skip other points
                if segment_started:
                    output_paths.append(overlapping)
                    overlapping = ""
                segment_started = False
        if segment_started:
            output_paths.append(overlapping)

    return output_paths


def divide_pathstring_parts(pathstring):
    """breaks single path string into substrings at each 'M' returning a list of path strings"""
    substring = pathstring.strip()
    paths = []
    while 'M' in substring[1:]:
        m_index = substring.find('M', 1)
        if m_index > -1:
            subpath = substring[0:m_index].strip()
            paths.append(subpath)
            substring = substring[m_index:].strip()

    paths.append(substring)
    return paths


# TODO: split open/closed separation into smaller chunks


def separate_closed_paths(paths):
    """takes a list of path strings
    breaks non continuous paths and
    joins connecting paths together
    to return a list of closed paths """
    discrete_paths = []
    closed_paths = []
    open_paths = []
    dead_ends = []
    for path in paths:
        discrete_paths += divide_pathstring_parts(path)
    for path in discrete_paths:
        parsed_path = SVGPT.parse_path(path)
        if parsed_path.isclosed():
            closed_paths.append(path)
        else:
            open_paths.append(parsed_path)
    while open_paths:
        path = open_paths.pop()
        # print(path)
        new_path = None
        for other_path in open_paths:
            if path.end == other_path.start:
                new_path = path.d() + " " + other_path.d().replace('M', 'L')
                open_paths.remove(other_path)
                break
            elif path.start == other_path.end:
                new_path = other_path.d() + " " + path.d().replace('M', 'L')
                open_paths.remove(other_path)
                break
            elif path.end == other_path.end:
                new_path = path.d() + " " + other_path.reversed().d().replace('M', 'L')
                open_paths.remove(other_path)
                break
            elif path.start == other_path.start:
                new_path = path.reversed().d() + " " + other_path.d().replace('M', 'L')
                open_paths.remove(other_path)
                break
        if new_path is not None:
            parsed_new_path = SVGPT.parse_path(new_path)
            if parsed_new_path.isclosed():
                closed_paths.append(new_path)
            else:
                open_paths.append(parsed_new_path)
            # print(new_path)
        else:
            dead_ends.append(path.d())

    open_paths = dead_ends
    return closed_paths, open_paths


if __name__ == "__main__":
    PATHS, ATTRIB = SVGPT.svg2paths("input-samples/test9-01.svg")
    PATH_STRINGS = []
    for apath in PATHS:
        PATH_STRINGS.append(apath.d())
    print(PATH_STRINGS)
