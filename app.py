# Import libraries
import os
from flask import Flask, render_template, jsonify
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_cors import CORS
from config import LocalDevelopmentConfig
import flask_excel
import json
from celery import shared_task
from celery.schedules import crontab
from database.models import db, make_data, MetaData, Customer, Offer, Professional, Work, your_works, report_helper

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
cache = Cache(app)
app.cache = cache
CORS(app, resources={r"/*": {"origins": "*"}})


#imoprt celery related things
from celery import Celery, Task
def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(LocalDevelopmentConfig)
    return celery_app

app.app_context().push()
celery_app = celery_init_app(app)
db.create_all()
make_data()
app.config.from_object(LocalDevelopmentConfig)


celery_app = Celery(
    'app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
    include=['endpoints.admin']  # Include tasks module
)


from endpoints.auth import auth_router
from endpoints.admin import admin
from endpoints.customer import customer
from endpoints.professional import professional
# Register the router
app.register_blueprint(auth_router, url_prefix = '/auth')
app.register_blueprint(admin, url_prefix = '/admin')
app.register_blueprint(customer, url_prefix = '/customer')
app.register_blueprint(professional, url_prefix = '/professional')
# Create the tables if they don't exist


flask_excel.init_excel(app)

@shared_task(ignore_result=True)
def send_email(to, subject, content):
    send_email(to, subject, content)

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=17, minute=0), request_reminder.s(), name='request_reminder')
    sender.add_periodic_task(crontab(day=1,hour=17, minute=0), monthly_report.s() , name='monthly_report')
from mail_service import send_email
import datetime

@celery_app.task
def request_reminder():
    for cust in Customer.query.all():
        offers=[]
        for offer in Offer.query.filter_by(target=cust.id).all():
            if offer.status=='pending':
                offers.append(offer.work_name)
        offers=set(offers)
        if cust.email is not None and offers:
            send_email(cust.email, 'Request Reminder', f'Dear {cust.name}, Please check your dashboard for the following work requests(s): {offers}')
    return 'done'

@celery_app.task
def monthly_report():
    for prof in Professional.query.all():
        if prof.email is not None:
            works_data = report_helper(prof.id)
    
            # If works_data is a Response object, extract the JSON
            if hasattr(works_data, 'get_json'):
                works = works_data.get_json()
            elif isinstance(works_data, str):
                works = json.loads(works_data)
            else:
                works = works_data
            send_email(prof.email, 'Monthly Report', f'Dear {prof.name}, Please check your monthly report {render_template("monthly_report.html",works=works)}')
    return 'done'

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
