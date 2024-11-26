# Import libraries
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import time
# Import the database and models
from database.models import db, Customer, Professional
from functools import wraps

professional = Blueprint('professional', __name__)


def approval_required(fn):
    @wraps(fn)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        professional = Professional.query.filter_by(id=user_id).first()
        if (not professional) or  professional.approval=="F":
            return jsonify(message="Access denied: Professional not approved"), 403
        return fn(*args, **kwargs)
    return decorated_function

@professional.route('/discover', methods=['POST', 'GET'], endpoint='professional-discover')
@approval_required
def professional_discover():
    return jsonify({'message': 'Professional discover'})


@professional.route('/your_work', methods=['POST', 'GET'], endpoint='professional-your-work')
@approval_required
def professional_your_work():
    return jsonify({'message': 'Professional your work'})


@professional.route('/profile', methods=['POST', 'GET'], endpoint='professional-profile')
@approval_required
def professional_profile():
    return jsonify({'message': 'Professional profile'})