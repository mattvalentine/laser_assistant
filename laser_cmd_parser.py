# laser_cmd_parser.py
"""Parses command line arguments for laser_assistant"""

import os
import argparse
from joint_generators import FlatJoint, BoxJoint, TslotJoint


def parse_command():
    """Parses arguements and returns constants."""
    parameters = {}

    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--output")
    parser.add_argument("--thickness")
    parser.add_argument("--segments")
    parser.add_argument("--kerf")
    parser.add_argument("--jointtype")
    parser.add_argument("--tsize")
    parser.parse_args()

    args = parser.parse_args()

    if args.input:
        input_file = args.input
    else:
        input_file = 'input-samples/test8-01.svg'
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        exit()

    if args.output:
        output_file = args.output
    else:
        output_file = 'output.svg'

    if args.thickness:
        thickness = float(args.thickness)
    else:
        thickness = 5
    if thickness <= 0:
        print(f"Invalid thickness: {thickness}")
        exit()

    if args.segments:
        segments = int(args.segments)
    else:
        segments = 5

    if args.kerf:
        kerf = float(args.kerf)
    else:
        kerf = 1.0
    if kerf < 0:
        print(f"Invalid kerf size (Must be positive or 0): {kerf}")
        exit()

    if args.jointtype:
        joint_type = str(args.jointtype)
    else:
        joint_type = 'tslot'

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

    parameters['thickness'] = thickness
    parameters['segments'] = segments
    parameters['kerf'] = kerf
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

    return(input_file, output_file, parameters)
