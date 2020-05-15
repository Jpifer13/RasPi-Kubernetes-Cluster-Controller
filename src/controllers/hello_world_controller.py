import requests

from flask import render_template
from flask import Blueprint, jsonify
import connexion

hello_world_controller = Blueprint( 'hello_world_controller', __name__ )

@hello_world_controller.route( '/hello-world', methods = [ 'GET' ])
def hello_world():
    """
    Render a hello world html template page
    """
    return render_template('hello_world.html', title='Main')