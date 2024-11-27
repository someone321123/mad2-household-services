# Import libraries
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import time
# Import the database and models
from database.models import db, Customer, Professional, Offer ,Work
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from functools import wraps
from datetime import datetime
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
    if request.method == 'POST':
        opr = request.json.get('operation')
        oid = request.json.get('offer_id')
        od_amount=request.json.get('amount')
        od_date=datetime.strptime(request.json.get('date'), '%Y-%m-%d')
        cid = get_jwt_identity()
        if Offer.query.filter_by(id=oid).first():
            offl=Offer.query.filter_by(id=oid)
            offer =offl.first()
            work_name=offer.work_name
            workl = Work.query.filter_by(name=offer.work_name)
            if opr=='accept':
                if offer.target==cid and offer.status=='pending':
                    try:
                        Offer.query.filter_by(work_name=offer.work_name).update({'status': 'rejected'})
                        logging.info('Successfully updated Offers with work_name = %s to status = rejected', work_name)
                    except Exception as e:
                        logging.error('Error updating Offers with work_name = %s: %s', work_name, e)

                    # 2. Update the Work where name matches
                    try:
                        workl.update({'status': 'closed', 'amount': od_amount, 'date': od_date})
                        logging.info('Successfully updated Work with name = %s to status = closed, amount = %s, date = %s', work_name, od_amount, od_date)
                    except Exception as e:
                        logging.error('Error updating Work with name = %s: %s', work_name, e)

                    # 3. Update the Offer where id matches
                    try:
                        offl.update({'status': 'accepted'})
                        logging.info('Successfully updated Offer with id = %s to status = accepted', oid)
                    except Exception as e:
                        logging.error('Error updating Offer with id = %s: %s', oid, e)
                    db.session.commit()

                    return jsonify({'message': 'Offer accepted'})
                else:
                    return jsonify({'message': 'Offer cant be accepted1'})
            elif opr=='reject':
                if (offer.target==cid or offer.source ==cid) and (offer.status=='pending'): 
                    offl.update({'status': 'rejected'})
                    logging.info('Successfully updated Offer with id = %s to status = rejected', oid)
                    db.session.commit()
                    return jsonify({'message': 'Offer rejected'})
                else:
                    return jsonify({'message': 'Offer cant be rejected2'})
            elif opr=='abandon':
                if (offer.target==cid or offer.source ==cid) and offer.status=='accepted':
                    workl.update({'status':'open'})
                    offl.update({'status': 'rejected'})
                    logging.info('Successfully updated Offer with id = %s to status = rejected', oid)
                    db.session.commit()
                    return jsonify({'message': 'Offer abandoned'})
                else:
                    return jsonify({'message': 'Offer cant be abandoned'})
            else:
                return jsonify({'message': 'Invalid operation'})
        else:   
            return jsonify({'message': 'No offer with this id'})
    return jsonify({'message': 'Professional your work'})


@professional.route('/profile', methods=['POST', 'GET'], endpoint='professional-profile')
@approval_required
def professional_profile():
    if request.method == 'POST':
        Professional.query.filter_by(id=get_jwt_identity()).update({'city': request.json.get('city')})
        db.session.commit()
        return jsonify({'message': 'City updated'})
    return jsonify({'message': 'Professional profile'})