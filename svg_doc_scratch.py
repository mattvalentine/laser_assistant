"""trying out the doc path tool"""

from svgpathtools import svg2paths2
paths, attributes, svg_attributes = svg2paths2('input-samples/test5-01.svg')
print(svg_attributes)
for i in range(len(paths)):
    print(paths[i])
    print(attributes[i])
# print(paths)
# print(attributes)
