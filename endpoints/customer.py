# Import libraries
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import time
from endpoints.auth import role_required
from datetime import datetime
from database.models import db, Customer, Professional, Offer, Location, Service, func, Work
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
    return jsonify({'message': 'Customer my work'})


@customer.route('/profile', methods=['POST', 'GET'], endpoint='customer-profile')
@role_required('customer') 
def customer_profile():
    name = Customer.query.filter_by(id=get_jwt_identity()).first().name
    city = Customer.query.filter_by(id=get_jwt_identity()).first().city
    return jsonify({'name': name, 'city': city})
    