# Import libraries
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import time
from endpoints.auth import role_required
# Import the database and models
from database.models import db, Customer, Professional, Offer,MetaData, func, Work,get_professionals_data
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
admin = Blueprint('admin', __name__)
@admin.route('/dashboard', methods = ['POST','GET'], endpoint = 'admin-dashboard')
@role_required('admin')  
def admin_dashboard():
    if request.method == 'POST':
        try:
            prof = request.json.get('professional_id')
            approval = request.json.get('approval')   #"T" or "F"
        except:
            return jsonify({'message': 'Invalid operation get'}), 400
        if approval == "T":
            profe = Professional.query.filter_by(id=prof).first()
            profe.approval = "T"
            db.session.commit()
            return jsonify({'message': 'Professional approved'})
        elif approval == "F":
            profe = Professional.query.filter_by(id=prof).first()
            profe.approval = "F"
            try:
                Offer.query.filter_by(source=prof, status='pending').update({'status': 'rejected'})
                logging.info('Updated Offer records where source = %s and status = pending', prof)
            except Exception as e:
                logging.error('Error updating Offer records for source = %s and status = pending: %s', prof, e)

            try:
                Offer.query.filter_by(target=prof, status='pending').update({'status': 'rejected'})
                logging.info('Updated Offer records where target = %s and status = pending', prof)
            except Exception as e:
                logging.error('Error updating Offer records for target = %s and status = pending: %s', prof, e)
            
            try:
                Offer.query.filter_by(source=prof, status='accepted').update({'status': 'rejected'})
                logging.info('Updated Offer records where source = %s and status = accepted', prof)
            except Exception as e:
                logging.error('Error updating Offer records for source = %s and status = pending: %s', prof, e)

            try:
                Offer.query.filter_by(target=prof, status='accepted').update({'status': 'rejected'})
                logging.info('Updated Offer records where target = %s and status = accepted', prof)
            except Exception as e:
                logging.error('Error updating Offer records for target = %s and status = pending: %s', prof, e)

            try:
                accepted_offer = Offer.query.filter_by(source=prof, status='accepted').first()
                if accepted_offer:
                    Work.query.filter_by(name=accepted_offer.work_name).update({'status': 'open'})
                    logging.info('Updated Work record where work = %s', accepted_offer.work_name)
                else:
                    logging.warning('No accepted offer found for source = %s', prof)
            except Exception as e:
                logging.error('Error updating Work record for source = %s and accepted status: %s', prof, e)

            try:
                accepted_offer = Offer.query.filter_by(target=prof, status='accepted').first()
                if accepted_offer:
                    Work.query.filter_by(name=accepted_offer.work_name).update({'status': 'open'})
                    logging.info('Updated Work record where work = %s', accepted_offer.work_name)
                else:
                    logging.warning('No accepted offer found for target = %s', prof)
            except Exception as e:
                logging.error('Error updating Work record for target = %s and accepted status: %s', prof, e)

            db.session.commit()
            return jsonify({'message': 'Professional unapproved'})
        else:
            return jsonify({'message': 'Invalid approval'})
    return get_professionals_data()

@admin.route('/statistics', methods=['POST', 'GET'], endpoint='admin-statistics')
@role_required('admin')  
def admin_statistics():
    if request.method == 'POST':
        try:
            entity = request.json.get('entity')
            if entity == "service":
                service=request.json.get('service')
                base=request.json.get('base')
                db.session.add(MetaData(name=service, info=base,dtype='service'))
                db.session.commit()
                return jsonify({'message': 'Service added'})
            elif entity == "location":
                city=request.json.get('city')
                state = request.json.get('state')
                db.session.add(MetaData(name=city, info=state,dtype='city'))
                db.session.commit()
                return jsonify({'message': 'Location added'})
            else:
                return jsonify({'message': 'Invalid entity'})
        except Exception as e:
            return jsonify({'message': f"Error: {str(e)}"}), 500
    # Get the total number of rows 
    try:
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
    except Exception as e:
        return jsonify({'message': f"Error: {str(e)}"}), 500


@admin.route('/backend', methods=['POST', 'GET'], endpoint='admin-backend')
@role_required('admin')  
def admin_backend():
    return jsonify({'message': 'Admin backend'})