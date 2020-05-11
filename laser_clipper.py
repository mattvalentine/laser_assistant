# laser_clipper.py
"""polygon math using Clipper library for laser cutting"""
# http://www.angusj.com/delphi/clipper/documentation/Docs/Units/ClipperLib/Types/ClipType.htm

import pyclipper

SCALING_FACTOR = 1000


def get_difference(first, second):
    """Takes two list of loops (list of (x,y) points), and returns the difference"""
    clipper = pyclipper.Pyclipper()
    scaled_first = pyclipper.scale_to_clipper(first, SCALING_FACTOR)
    scaled_second = pyclipper.scale_to_clipper(second, SCALING_FACTOR)

    clipper.AddPaths(scaled_first, pyclipper.PT_SUBJECT)
    clipper.AddPaths(scaled_second, pyclipper.PT_CLIP)
    scaled_difference = clipper.Execute(pyclipper.CT_DIFFERENCE)

    difference = pyclipper.scale_from_clipper(
        scaled_difference, SCALING_FACTOR)
    return difference


def get_intersection(first, second):
    """Takes two list of loops(list of(x, y) points), and returns the intersection"""
    clipper = pyclipper.Pyclipper()  # pylint: disable=c-extension-no-member
    scaled_first = pyclipper.scale_to_clipper(first, SCALING_FACTOR)
    scaled_second = pyclipper.scale_to_clipper(second, SCALING_FACTOR)

    clipper.AddPaths(scaled_first, pyclipper.PT_SUBJECT)
    clipper.AddPaths(scaled_second, pyclipper.PT_CLIP)
    scaled_intersection = clipper.Execute(pyclipper.CT_INTERSECTION)

    intersection = pyclipper.scale_from_clipper(
        scaled_intersection, SCALING_FACTOR)
    return intersection


def get_union(first, second):
    """Takes two list of loops(list of(x, y) points), and returns the union"""
    clipper = pyclipper.Pyclipper()  # pylint: disable=c-extension-no-member
    scaled_first = pyclipper.scale_to_clipper(first, SCALING_FACTOR)
    scaled_second = pyclipper.scale_to_clipper(second, SCALING_FACTOR)

    clipper.AddPaths(scaled_first, pyclipper.PT_SUBJECT)
    clipper.AddPaths(scaled_second, pyclipper.PT_CLIP)
    scaled_union = clipper.Execute(pyclipper.CT_UNION)

    union = pyclipper.scale_from_clipper(
        scaled_union, SCALING_FACTOR)
    return union


def get_xor(first, second):
    """Takes two list of loops(list of(x, y) points), and returns the exclusive-or"""
    clipper = pyclipper.Pyclipper()  # pylint: disable=c-extension-no-member
    scaled_first = pyclipper.scale_to_clipper(first, SCALING_FACTOR)
    scaled_second = pyclipper.scale_to_clipper(second, SCALING_FACTOR)

    clipper.AddPaths(scaled_first, pyclipper.PT_SUBJECT)
    clipper.AddPaths(scaled_second, pyclipper.PT_CLIP)
    scaled_xor = clipper.Execute(pyclipper.CT_XOR)

    xor = pyclipper.scale_from_clipper(
        scaled_xor, SCALING_FACTOR)
    return xor


def get_offset_loop(shape, offset_size):
    """takes a list of loops (list of(x, y) points), and returns loops offset by a given size"""
    offsetter = pyclipper.PyclipperOffset()
    scaled_shape = pyclipper.scale_to_clipper(shape, SCALING_FACTOR)
    scaled_offset_size = offset_size * SCALING_FACTOR

    offsetter.AddPaths(scaled_shape, pyclipper.JT_ROUND, pyclipper.PT_SUBJECT)
    scaled_offset = offsetter.Execute(scaled_offset_size)

    offset = pyclipper.scale_from_clipper(scaled_offset, SCALING_FACTOR)
    return offset


def point_inside_loop(point, loop):
    """tests to see if a point is inside (1), on(-1), or outside (0) of a loop"""
    scaled_loop = pyclipper.scale_to_clipper(loop, SCALING_FACTOR)
    scaled_point = [int(point[0]*SCALING_FACTOR), int(point[1]*SCALING_FACTOR)]
    is_point_inside = pyclipper.PointInPolygon(scaled_point, scaled_loop)
    return is_point_inside
