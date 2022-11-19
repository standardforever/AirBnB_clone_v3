#!/usr/bin/python3
'''objects that handles all default RESTFul API actions'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


HTTP_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
'''http Methods'''


@app_views.route('/amenities', methods=HTTP_METHODS)
@app_views.route('/amenities/<amenity_id>', methods=HTTP_METHODS)
def handle_amenities(amenity_id=None):
    '''http method handler for the amenities endpoint.
    '''
    handlers = {
        'GET': get_amenities,
        'DELETE': remove_amenity,
        'POST': add_amenity,
        'PUT': update_amenity,
    }
    if request.method in handlers:
        return handlers[request.method](amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_amenities(amenity_id=None):
    '''Gets the amenity by id or all amenities.
    '''
    amenities = storage.all(Amenity).values()
    if amenity_id:
        res = list(filter(lambda x: x.id == amenity_id, amenities))
        if res:
            return jsonify(res[0].to_dict())
        raise NotFound()
    amenities = list(map(lambda x: x.to_dict(), amenities))
    return jsonify(amenities)


def remove_amenity(amenity_id=None):
    '''Removes a amenity by id.
    '''
    amenities = storage.all(Amenity).values()
    res = list(filter(lambda x: x.id == amenity_id, amenities))
    if res:
        storage.delete(res[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_amenity(amenity_id=None):
    '''creates new amenity.
    '''
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


def update_amenity(amenity_id=None):
    '''Updates the amenity by id.
    '''
    ignored_keys = ('id', 'created_at', 'updated_at')
    amenities = storage.all(Amenity).values()
    res = list(filter(lambda x: x.id == amenity_id, amenities))
    if res:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        old_amenity = res[0]
        for key, value in data.items():
            if key not in ignored_keys:
                setattr(old_amenity, key, value)
        old_amenity.save()
        return jsonify(old_amenity.to_dict()), 200
    raise NotFound()
