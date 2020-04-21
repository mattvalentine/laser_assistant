"""
  polygon_math_tests -- testing python modules for polygon operations.
  Particularly:
  - booleans (union / difference) -- used for tabs, slots, etc.
    --> we need very robust operations!
    --> Support for lots of line segments [e.g. for curved edges] also a plus.
    --> should have a way to specify a tolerance (e.g., 0.001mm) and be accurate within that.
  - offsetting -- used for fit adjustment and kerf.
    --> we need per-edge offset values!
    --> support for dogbones also a plus, but could be applied as a post-process.
"""

import math


#-----------------------------------------------

#helpers to create geometry quickly:
#NOTE: geometry here will always be tuples of loops, where loops are either CCW-oriented [outer] or CW-oriented [inner / holes] lists of points.

def rect(x,y,w,h):
    assert(w > 0)
    assert(h > 0)
    return ( ((x,y), (x+w,y), (x+w,y+h), (x,y+h)), )

def circle(x,y,r):
    assert(r > 0)
    steps = 360/5 #<-- 5-degree steps
    ret = []
    for step in range(0,steps):
        ang = step / steps * math.PI
        ret.append( (x + math.cos(ang), y + math.sin(ang)) )
    return ( tuple(ret), )

#-----------------------------------------------
#The tests themselves:

tests = []

#Take the difference of two boxes:
def test_simple_difference(math,output):
    boxA = rect(0,0, 40, 60)
    boxB = rect(20,10, 40, 60)

    out = math.difference(boxA, boxB)

    output.draw(boxA, layer="inputA")
    output.draw(boxB, layer="inputB")
    output.draw(out, layer="output")

tests.append(test_simple_difference)

#Take the difference of two boxes:
def test_simple_union(math,output):
    boxA = rect(0,0, 40, 60)
    boxB = rect(20,10, 40, 60)

    out = math.union(boxA, boxB)

    output.draw(boxA, layer="inputA")
    output.draw(boxB, layer="inputB")
    output.draw(out, layer="output")

tests.append(test_simple_union)

#Subtract a joint from a box
def test_box_joint(math, output):
    box = rect(0,0,40,60)
	# simulation of simple box joint
    joint = (((40, 0), (40, 20), (38, 20), (38, 40), (40, 40), (40, 60)), )

	# new closed loop with joint cut out
    out1 = math.difference(box, joint)
	# new shape from negative space
    out2 = math.difference(box, out1)

    output.draw(box, layer="inputA")
    output.draw(joint, layer="inputB")
    output.draw(out1, layer="output")
    output.draw(out2, layer="output2")


tests.append(test_box_joint)

def test_offset(math, output):
    box = rect(0,0,40,60)

    offset = 1.0
    out = math.offset(box, offset)

    output.draw(box, layer="inputA")
    output.draw(out, layer="output")

tests.append(test_offset)

def test_kerfed_box_joint(math, output):
    box = rect(0,0,40,60)
	# simulation of simple box joint
    joint = (((40, 0), (40, 20), (38, 20), (38, 40), (40, 40), (40, 60)), )
	# new closed loop with joint cut out
    out1 = math.difference(box, joint)

    offset = 1.0
    kerfbox = math.offset(box, offset)

    kerfout = math.offset(out1, offset)

	# new shape from negative space
    diff = math.difference(kerfbox, kerfout)

    output.draw(box, layer="inputA")
    output.draw(joint, layer="inputB")
    output.draw(out1, layer="output")
    output.draw(kerfout, layer="output2")
    output.draw(diff, layer="output3")

tests.append(test_kerfed_box_joint)

#-----------------------------------------------
#Classes passed to the tests:

class NoMath:
    """Math implementation that doesn't actually do anything!"""
    def union(self, A,B):
        return ( (), )
    def difference(self, A,B):
        return ( (), )

import pyclipper
class ClipperMath:
    """Math implementation that uses pyclipper"""
    SCALING_FACTOR = 1000 #clipper uses integer coordinates; this scale factor results in 0.001mm precision
    def union(self, A,B):
        pc = pyclipper.Pyclipper()
        pc.AddPaths(pyclipper.scale_to_clipper(A, ClipperMath.SCALING_FACTOR), pyclipper.PT_SUBJECT)
        pc.AddPaths(pyclipper.scale_to_clipper(B, ClipperMath.SCALING_FACTOR), pyclipper.PT_CLIP)
        return pyclipper.scale_from_clipper(pc.Execute(pyclipper.CT_UNION), ClipperMath.SCALING_FACTOR)
    def difference(self, A,B):
        pc = pyclipper.Pyclipper()
        pc.AddPaths(pyclipper.scale_to_clipper(A, ClipperMath.SCALING_FACTOR), pyclipper.PT_SUBJECT)
        pc.AddPaths(pyclipper.scale_to_clipper(B, ClipperMath.SCALING_FACTOR), pyclipper.PT_CLIP)
        return pyclipper.scale_from_clipper(pc.Execute(pyclipper.CT_DIFFERENCE), ClipperMath.SCALING_FACTOR)
    def intersection(self, A,B):
        pc = pyclipper.Pyclipper()
        pc.AddPaths(pyclipper.scale_to_clipper(A, ClipperMath.SCALING_FACTOR), pyclipper.PT_SUBJECT)
        pc.AddPaths(pyclipper.scale_to_clipper(B, ClipperMath.SCALING_FACTOR), pyclipper.PT_CLIP)
        return pyclipper.scale_from_clipper(pc.Execute(pyclipper.CT_INTERSECTION), ClipperMath.SCALING_FACTOR)
    def offset(self, A, offset_size):
        pco = pyclipper.PyclipperOffset()
        pco.AddPaths(pyclipper.scale_to_clipper(A, ClipperMath.SCALING_FACTOR), pyclipper.JT_ROUND, pyclipper.PT_SUBJECT)
        scaled_size = offset_size * ClipperMath.SCALING_FACTOR
        return pyclipper.scale_from_clipper(pco.Execute(scaled_size), ClipperMath.SCALING_FACTOR)

class SVGOutput:
    """Write output to an SVG for viewing."""
    def __init__(self, styles = dict()):
        """
        the 'styles' parameter is a dictionary of styles applied to each layer to make the output clearer.
        """
        self.styles = styles
        self.layers = dict()
    
    def draw(self, loops, layer="none"):
        if layer not in self.layers:
            self.layers[layer] = []
        self.layers[layer].append(loops)

    def write(self, filename):
        #compute bounding box:
        min_x = min_y = float('inf')
        max_x = max_y = -float('inf')

        for layer in self.layers.values():
            for loops in layer:
                for loop in loops:
                    for pt in loop:
                        min_x = min(min_x, pt[0])
                        min_y = min(min_y, pt[1])
                        max_x = max(max_x, pt[0])
                        max_y = max(max_y, pt[1])

        #if drawing is empty, set to [0,0]x[0,0] box:
        if min_x > max_x: min_x = max_x = 0
        if min_y > max_y: min_y = max_y = 0

        #make drawing edges lie on a 10mm grid, offset by 2.5mm so that 1cm grid lines don't end up exactly at the edge of the page:
        min_x = math.floor(min_x / 10) * 10 - 2.5
        min_y = math.floor(min_y / 10) * 10 - 2.5
        max_x = math.ceil(max_x / 10) * 10 + 2.5
        max_y = math.ceil(max_y / 10) * 10 + 2.5

        #write out to svg:
        with open(filename, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
            f.write(b'<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
            f.write(f'<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="{max_x-min_x}mm" height="{max_y-min_y}mm" viewBox="{min_x} {min_y} {max_x-min_x} {max_y-min_y}">\n'.encode('utf8'))
            for name,layer in self.layers.items():
                if name in self.styles:
                    style = self.styles[name]
                elif '' in self.styles:
                    style = self.styles['']
                else:
                    style = ''
                #NOTE: the inkscape: attributes here are a convenience to make the groups appear in the inkscape 'layers' dropdown.
                f.write(f'<g id="{name}" inkscape:groupmode="layer" inkscape:label="{name}">\n'.encode('utf8'))
                for loops in layer:
                    f.write(f'<path style="{style}" d=\"'.encode('utf8'))
                    for loop in loops:
                        data = 'M'
                        for pt in loop:
                            data += f' {pt[0]} {pt[1]}'
                        data += 'Z'
                        f.write(data.encode('utf8'))
                    f.write(b'\" />\n')

                f.write(b'</g>\n')

            f.write(b'</svg>\n')


#-----------------------------------------------
#Code that actually runs the tests:

for Math in [ClipperMath]:
    for test in tests:
        filename = test.__name__ + "." + Math.__name__ + ".svg"

        print("----- " + filename + " -----")
        baseStyle = 'fill-opacity:0.5; fill-rule:evenodd; stroke-width:0.5; stroke-linejoin:round; stroke-linecap:round;'
        output = SVGOutput({
            ''      :'fill:#f0f; stroke:#f0f; ' + baseStyle,
            'inputA':'fill:#00f; stroke:#00f; ' + baseStyle,
            'inputB':'fill:#f00; stroke:#f00; ' + baseStyle,
            'output':'fill:#0f0; stroke:#0f0; ' + baseStyle,
    		'output2':'fill:#ff0; stroke:#ff0; ' + baseStyle,
    		'output3':'fill:#0ff; stroke:#0ff; ' + baseStyle
        });
        test(Math(), output)
        output.write(filename)

