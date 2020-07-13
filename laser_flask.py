"""Flask server to host UI"""

# Run with these commands:
# export FLASK_APP=laser_flask.py
# flask run

from flask import Flask, request, redirect, jsonify
from flask_cors import CORS

# it's common practice to use lowercase app, so we'll ignore pep8 just this once
app = Flask(__name__)  # pylint: disable=invalid-name
app.config['CORS_HEADERS'] = 'Content-Type'

# Allow VUE client to make requests to this API server
VUE_CLIENT = {"origins": "http://localhost:8080"}
cors = CORS(app, resources={r"*": VUE_CLIENT})  # pylint: disable=invalid-name


@app.route('/')
def main_interface():
    """This is the root of the html interface"""
    # redirects to VUE app
    return redirect('http://localhost:8080/')


@app.route('/parameters', methods=['POST'])
def parameters():
    """takes the params and writes them to a file"""
    params = request.form
    print(params)
    return jsonify(params)


@app.route('/edge_click')
def svgclick():
    """reacts to the click of an svg element"""
    edge_args = request.args
    print(edge_args)
    return jsonify(edge_args)


@app.route('/get_output')
def get_output():
    """returns output.svg"""
    return get_svg_response('output.svg')


@app.route('/get_edges')
def get_edges():
    """returns edges.json"""
    # return get_svg_response('edges.svg')
    return get_json_response('edges.json')


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


def get_json_response(filename):
    """returns a response with json object"""
    jsonfile = open(filename, "r")
    jsondata = jsonfile.read()
    jsonfile.close()
    response = app.response_class(
        response=jsondata,
        status=200,
        mimetype='application/json'
    )
    return response
