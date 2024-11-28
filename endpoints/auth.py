# Import libraries
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,  get_jwt
import time
# Import the database and models
from database.models import db, Customer, Professional

auth_router = Blueprint('auth', __name__)

# Routes
@auth_router.route('/login', methods = ['POST'], endpoint = 'auth-login')
def login():
    try:
        data = request.get_json()
        name = data.get('name')
        password = data.get('password')

        if Professional.query.filter_by(name = name).first():
            user = Professional.query.filter_by(name = name).first()
        else:
            user = Customer.query.filter_by(name = name).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity = user.id, additional_claims={'role': user.role})
            return jsonify(access_token = access_token,role=user.role)
        else:
            return jsonify({ 'message': 'Invalid credentials' }), 401
    except Exception as e:
        return jsonify({ 'message': 'An unexpected error occurred', 'error': str(e) }), 500

###########
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
import uuid  # For unique id generation


@auth_router.route('/register', methods=['POST','GET'], endpoint='auth-register')
def register():
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'message': 'Invalid request: JSON data missing'}), 400
            
            # Extract and validate data
            username = data.get('name')
            password = data.get('password')
            service = data.get('service')
            city = data.get('city')
            email=data.get('email')
            if not username or not password:
                return jsonify({'message': 'Username and password are required'}), 400
            if service:  # Professional registration
                if Professional.query.filter_by(name=username).first():
                    return jsonify({'message': 'Username already in use'}), 400
                new_user = Professional(
                    name=username,
                    service=service, 
                    city=city,
                    approval='F',
                    email=email
                )
            else:  # Customer registration
                if Customer.query.filter_by(name=username).first():
                    return jsonify({'message': 'Username already in use'}), 400
                new_user = Customer(
                    name=username,
                    city=city,
                    email=email
                )
            db.session.add(new_user)
            db.session.commit()
            # Hash the password and save the user
            if hasattr(new_user, 'set_password'):
                new_user.set_password(password)
                db.session.commit()
            else:
                return jsonify({'message': 'Password hashing method not implemented'}), 500
            # Login the new user after registration
            return jsonify({
                'message': 'User registered successfully',
                
            }), 201

        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'message': 'Database error', 'error': str(e)}), 500
        except Exception as e:
            return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

from functools import wraps
from flask import jsonify

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()  # First, ensure the user is authenticated
        def decorated_function(*args, **kwargs):
            # Get the user's role from the token claims
            claims = get_jwt()
            if claims.get('role') != required_role:
                return jsonify(message="Access denied: insufficient permissions"), 403
            return fn(*args, **kwargs)
        return decorated_function
    return wrapper