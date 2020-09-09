# #!/bin/bash

if [ ! -d "/svgpathtools" ] 
then
  git clone https://github.com/mathandy/svgpathtools.git
  python svgpathtools/setup.py install
fi


python3 laser_flask.py

# export FLASK_APP=laser_flask.py
# flask run