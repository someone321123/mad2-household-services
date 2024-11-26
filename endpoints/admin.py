# Import libraries
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import time
from endpoints.auth import role_required
# Import the database and models
from database.models import db, Customer, Professional, Offer, Location, Service, func, Work

admin = Blueprint('admin', __name__)
@admin.route('/dashboard', methods = ['POST','GET'], endpoint = 'admin-dashboard')
@role_required('admin')  
def admin_dashboard():
    if request.method == 'POST':
        prof = request.json.get('professional_id')
        approval = request.json.get('approval')   #"T" or "F"
        if approval == "T":
            profe = Professional.query.filter_by(id=prof).first()
            profe.approval = "T"
            db.session.commit()
            return jsonify({'message': 'Professional approved'})
        elif approval == "F":
            profe = Professional.query.filter_by(id=prof).first()
            profe.approval = "F"
            Offer.query.filter_by(source=prof).update({'status': 'rejected'})
            Offer.query.filter_by(target=prof).update({'status': 'rejected'})
            db.session.commit()
            return jsonify({'message': 'Professional unapproved'})
        else:
            return jsonify({'message': 'Invalid approval'})
    return jsonify({'message': 'Admin dashboard'})

@admin.route('/statistics', methods=['POST', 'GET'], endpoint='admin-statistics')
@role_required('admin')  
def admin_statistics():
    if request.method == 'POST':
        entity = request.json.get('entity')
        if entity == "service":
            service=request.json.get('service')
            base=request.json.get('base')
            db.session.add(Service(service, base))
            db.session.commit()
            return jsonify({'message': 'Service added'})
        elif entity == "location":
            city=request.json.get('city')
            state = request.json.get('state')
            db.session.add(Location(city=city, state=state))
            db.session.commit()
            return jsonify({'message': 'Location added'})
        else:
            return jsonify({'message': 'Invalid entity'})
    # Get the total number of rows 
    num_prof = db.session.query(func.count(Professional.id)).scalar() 
    num_cust = db.session.query(func.count(Professional.id)).scalar() 
    # # Get the highest and lowest entries based on a specific column (e.g., experience) 
    highest_prof= db.session.query(Professional).order_by(Professional.rating.desc()).first().name
    lowest_prof = db.session.query(Professional).order_by(Professional.rating).first().name

    done_count_work = db.session.query(func.count(Work.id)).filter_by(status='done').scalar()
    not_done_count_work = db.session.query(func.count(Work.id)).filter_by(status='open').scalar()
    done_count_offer = db.session.query(func.count(Offer.id)).filter_by(status='accepted').scalar()
    not_done_count_offer = db.session.query(func.count(Offer.id)).filter_by(status='rejected').scalar()

    return jsonify({'message': 'Admin statistics', 'num_prof': num_prof, 'num_cust': num_cust, 'highest_prof': highest_prof, 
                    'lowest_prof': lowest_prof, 'done_count_work': done_count_work, 'not_done_count_work': not_done_count_work, 
                    'done_count_offer': done_count_offer, 'not_done_count_offer': not_done_count_offer

                    })


@admin.route('/backend', methods=['POST', 'GET'], endpoint='admin-backend')
@role_required('admin')  
def admin_backend():
    return jsonify({'message': 'Admin backend'})