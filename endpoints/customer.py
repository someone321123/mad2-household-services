# Import libraries
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import time
from endpoints.auth import role_required
from datetime import datetime
from database.models import db, Customer, Professional, Offer, Location, Service, func, Work
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Import the database and models, 

customer = Blueprint('customer', __name__)
@customer.route('/new_work', methods=['POST', 'GET'], endpoint='customer-new-work')
@role_required('customer') 
def customer_new_work():
    if request.method == 'POST':
        opr = request.json.get('operation')
        if opr == "new":
            name = request.json.get('name')
            description = request.json.get('description')
            amount = request.json.get('amount')
            date = datetime.strptime(request.json.get('date'), '%Y-%m-%d')
            service = request.json.get('service')
            address = request.json.get('address')
            customer_id =get_jwt_identity()
            city = request.json.get('city')
            db.session.add(Work(name=name, description=description, amount=amount, date=date, service=service, address=address, status='open', customer_id=customer_id, city=city))
            db.session.commit()
            return jsonify({'message': 'Work created'})
        elif opr == "update":
            #work_id = request.json.get('name') #fixed
            name = request.json.get('name')
            description = request.json.get('description')
            amount = request.json.get('amount')
            try:
                date = datetime.strptime(request.json.get('date'), '%Y-%m-%d')
            except:
                pass
            service = request.json.get('service')
            address = request.json.get('address')
            #customer_id =get_jwt_identity()
            city = request.json.get('city')
            db.session.query(Work).filter_by(name=name).update({ 'description': description, 'amount': amount, 'date': date,
                                                                    'service': service, 'address': address,  'city': city})
            db.session.commit()
            return jsonify({'message': 'Work updated'})
        else:
            return jsonify({'message': 'Invalid operation'})
    return jsonify({'message': 'Customer new work'})


@customer.route('/my_work', methods=['POST', 'GET'], endpoint='customer-my-work')
@role_required('customer') 
def customer_my_work():
    if request.method == 'POST':
        work_name = request.json.get('work_name')
        target = request.json.get('target')
        o_amount= request.json.get('amount')
        od_date = datetime.strptime(request.json.get('date'), '%Y-%m-%d')
        source = get_jwt_identity()
        db.session.add(Offer(work_name=work_name, target=target, od_amount=o_amount, od_date=od_date, source=source))
        try:
            Offer.query.filter_by(source=target,work_name=work_name).first().update({'status': 'rejected'})
        except:
            pass
        db.session.commit()
        return jsonify({'message': 'Offer created'})


    return jsonify({'message': 'Customer my work'})


@customer.route('/my_work/update', methods=['POST', 'GET'], endpoint='customer-my-work-update')
@role_required('customer') 
def customer_my_work_update():
    if request.method == 'POST':
        opr = request.json.get('operation')
        oid = request.json.get('offer_id')
        work_name=Offer.query.filter_by(id=oid).first().work_name
        od_amount=request.json.get('amount')
        od_date=request.json.get('date')
        if opr=='accept':
            try:
                Offer.query.filter_by(work_name=work_name).update({'status': 'rejected'})
                logging.info('Successfully updated Offers with work_name = %s to status = rejected', work_name)
            except Exception as e:
                logging.error('Error updating Offers with work_name = %s: %s', work_name, e)

            # 2. Update the Work where name matches
            try:
                Work.query.filter_by(name=work_name).update({'status': 'closed', 'amount': od_amount, 'date': od_date})
                logging.info('Successfully updated Work with name = %s to status = closed, amount = %s, date = %s', work_name, od_amount, od_date)
            except Exception as e:
                logging.error('Error updating Work with name = %s: %s', work_name, e)

            # 3. Update the Offer where id matches
            try:
                Offer.query.filter_by(id=oid).update({'status': 'accepted'})
                logging.info('Successfully updated Offer with id = %s to status = accepted', oid)
            except Exception as e:
                logging.error('Error updating Offer with id = %s: %s', oid, e)

            return jsonify({'message': 'Offer accepted'})
@customer.route('/profile', methods=['POST', 'GET'], endpoint='customer-profile')
@role_required('customer') 
def customer_profile():
    if request.method == 'POST':
        Customer.query.filter_by(id=get_jwt_identity()).update({'city': request.json.get('city')})
        db.session.commit()
        return jsonify({'message': 'City updated'})
    name = Customer.query.filter_by(id=get_jwt_identity()).first().name
    city = Customer.query.filter_by(id=get_jwt_identity()).first().city
    return jsonify({'name': name, 'city': city})
    