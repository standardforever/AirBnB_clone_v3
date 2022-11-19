#!/usr/bin/python3
'''Flask web API.
'''
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
'''Flask application instance.'''
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': host}})


@app.teardown_appcontext
def teardown_flask(exception):
    '''method to handle @app.teardown_appcontext'''
    storage.close()


@app.errorhandler(404)
def error_404(error):
    '''Handles error 404 to return json'''
    return jsonify(error='Not found'), 404


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    app.url_map.strict_slashes = False
    app.register_blueprint(app_views)
    app.run(
        host=host if host else '0.0.0.0',
        port=port if port else '5000',
        threaded=True
    )
