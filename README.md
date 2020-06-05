# laser_assistant
A tool to generate joints for laser cutting

## Prerequisites
Currently **Python 3.7** is recommended for use of laser_assistant.

There are two main dependencies for this program, SVG Path Tools and PyClipper. It is **important not to use pip to install SVG Path Tools** because this program requires a newer version than pip offers. All other dependencies not listed below are standard Python libraries.

### [PyClipper](https://github.com/fonttools/pyclipper): 

```
pip install pyclipper
```

### [SVG Path Tools](https://github.com/mathandy/svgpathtools): 

```
git clone git@github.com:mathandy/svgpathtools.git; cd svgpathtools; python setup.py install
```


## Usage

### Simple test with sample input: 

```
python laser_assistant.py
```

This should run without errors taking `input-samples/test6-01.svg` as input and producing `output.svg` which has joints generated and kerf compensated paths.

### Command line options

```
usage: laser_assistant.py [-h] [--input INPUT] [--output OUTPUT]
                          [--thickness THICKNESS] [--segments SEGMENTS]
                          [--kerf KERF] [--jointtype JOINTTYPE]
                          [--tsize TSIZE]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT
  --output OUTPUT
  --thickness THICKNESS
  --segments SEGMENTS
  --kerf KERF
  --jointtype JOINTTYPE
  --tsize TSIZE
```
### Input file formatting

The current implementation requires SVG input files to be organized in layers (`<g>`) for the program to understand the organization of the model.

At the top layer There should be one layer for each component of the model or "face". Each should be named called `Face#` where `#` enumerates the faces(eg. `Face1`, `Face2`, etc), and each of those should have 3 sublayers called `Perimeter`, `Cuts`, and `Joints` which contains an additional sublayer for each "joint". 

`Perimeter` should contain a path that traces the outermost edge of the face, and `Cuts` should contain paths within the face to be cut out (if any). Joints are named with the convention `J#-X` where `#` enumerates the specific joint, and `X` is either `A` or `B` signifying which half of the joint this linear path represents. For example `Face1` might contain `J1-A`, and `Face2`'s joint layer might contain `J1-B` representing the joint that connects `Face1` to `Face2`. See the example in test8-01.svg for reference.

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 120">
    <g id="Face2">
        <g id="Perimeter">
            <rect x="150" y="10" width="100" height="100" style="fill:none;stroke:#2e3192;stroke-miterlimit:10;stroke-width:0.25px"/>
        </g>
        <g id="Cuts">
            <rect x="210" y="70" width="30" height="30" style="fill:none;stroke:#231f20;stroke-miterlimit:10;stroke-width:0.25px"/>
        </g>
        <g id="Joints"><g id="J1-A">
            <line x1="150" y1="110" x2="150" y2="10" style="fill:none;stroke:#00a651;stroke-miterlimit:10;stroke-width:0.25px"/>
        </g></g>
    </g>
    <g id="Face1">
        <g id="Perimeter-2" data-name="Perimeter">
            <rect x="10" y="10" width="100" height="100" style="fill:none;stroke:#2e3192;stroke-miterlimit:10;stroke-width:0.25px"/>
        </g>
        <g id="Cuts-2" data-name="Cuts">
            <rect x="30" y="40" width="20" height="20" style="fill:none;stroke:#231f20;stroke-miterlimit:10;stroke-width:0.25px"/>
            <rect x="40" y="70" width="20" height="30" style="fill:none;stroke:#231f20;stroke-miterlimit:10;stroke-width:0.25px"/>
        </g>
        <g id="Joints"><g id="J1-B">
            <line x1="110" y1="10" x2="110" y2="110" style="fill:none;stroke:#00a651;stroke-miterlimit:10;stroke-width:0.25px"/>
        </g>
        </g>
    </g>
</svg>
```



## Coming soon!
The next step is to assist the user in taking an unformatted SVG and breaking it down into faces, cuts, and joints. 

Stay tuned!