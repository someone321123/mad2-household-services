# Import libraries
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import time
# Import the database and models
from database.models import db, Customer, Professional
from functools import wraps
from datetime import datetime
from database.models import Offer
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
    if request.method == 'POST':
        work_name = request.json.get('work_name')
        target = int(request.json.get('target'))
        o_amount= request.json.get('amount')
        od_date = datetime.strptime(request.json.get('date'), '%Y-%m-%d')
        source = get_jwt_identity()
        db.session.add(Offer(work_name=work_name, target=target, od_amount=o_amount, od_date=od_date, source=source))
        db.session.commit()
        return jsonify({'message': 'Offer created'})
    return jsonify({'message': 'Professional discover'})


@professional.route('/your_work', methods=['POST', 'GET'], endpoint='professional-your-work')
@approval_required
def professional_your_work():
    return jsonify({'message': 'Professional your work'})


@professional.route('/profile', methods=['POST', 'GET'], endpoint='professional-profile')
@approval_required
def professional_profile():
    if request.method == 'POST':
        Professional.query.filter_by(id=get_jwt_identity()).update({'city': request.json.get('city')})
        db.session.commit()
        return jsonify({'message': 'City updated'})
    return jsonify({'message': 'Professional profile'})