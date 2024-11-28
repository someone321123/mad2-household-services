# Import libraries
import os
from flask import Flask, render_template, jsonify
from flask_jwt_extended import JWTManager

# Import routes
from endpoints.auth import auth_router
from endpoints.admin import admin
from endpoints.customer import customer
from endpoints.professional import professional
# Import utilities and other stuff
from database.models import db, make_data, MetaData
from flask_cors import CORS



# Define a Flask instance
app = Flask(__name__)

# Configure an SQLite database
db_path = os.path.join(os.path.dirname(__file__), 'database', 'site.db')    # Use absolute path to store SQLite database in some other location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)      # Ideally, this should not be hardcoded and read from an environment file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')    # Ideally, this should again be read from an env file and NOT hardcoded here
jwt = JWTManager(app)

# Initialize the database
db.init_app(app)


CORS(app, resources={r"/*": {"origins": "*"}})

# Register the router
app.register_blueprint(auth_router, url_prefix = '/auth')
app.register_blueprint(admin, url_prefix = '/admin')
app.register_blueprint(customer, url_prefix = '/customer')
app.register_blueprint(professional, url_prefix = '/professional')
# Create the tables if they don't exist
app.app_context().push()
db.create_all()
make_data()


@app.route('/hello_world', methods=['GET'])
def get_cities_and_services():
    cities = MetaData.query.filter_by(dtype='city').all()
    services = MetaData.query.filter_by(dtype='service').all()
    cities_data = [{'id': city.id, 'name': city.name,'state':city.info} for city in cities]
    services_data = [{'id': service.id, 'name': service.name, 'base': service.info} for service in services]
    return jsonify({'cities': cities_data, 'services': services_data})

if __name__ == '__main__':
    environment = os.environ.get('ENVIRONMENT', 'dev')
    host = '127.0.0.1' if environment == 'dev' else '0.0.0.0'
    debug = True if environment == 'dev' else False
    app.run(host = host, debug = debug, port=5000)
