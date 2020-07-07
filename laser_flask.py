"""Flask server to host UI"""

# Run with these commands:
# export FLASK_APP=laser_flask.py
# flask run

from flask import Flask, request, redirect, jsonify

# it's common practice to use lowercase app, so we'll ignore pep8 just this once
app = Flask(__name__)  # pylint: disable=invalid-name


@app.route('/')
def main_interface():
    """This is the root of the html interface"""
    # redirects to vue app
    return redirect('http://localhost:8080/')


@app.route('/parameters', methods=['POST'])
def parameters():
    """takes the params and writes them to a file"""
    params = request.form
    print(params)
    return jsonify(params)


@app.route('/svgclick')
def svgclick():
    """reacts to the click of an svg element"""
    svg_args = request.args
    print(svg_args)


@app.route('/get_output')
def get_output():
    """returns output.svg"""
    return get_svg_response('output.svg')


@app.route('/get_edges')
def get_edges():
    """returns edges.svg"""
    return get_svg_response('edges.svg')


def get_svg_response(filename):
    """returns a response with svg file"""
    svgfile = open(filename, "r")
    svgdata = svgfile.read()
    svgfile.close()
    response = app.response_class(
        response=svgdata,
        status=200,
        mimetype='image/svg+xml'
    )
    return response
