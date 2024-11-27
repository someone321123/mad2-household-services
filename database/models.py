
# Import libraries
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import time
db = SQLAlchemy()
from sqlalchemy import create_engine,func
import secrets
from datetime import datetime
from sqlalchemy import Float, Integer, String, Date, ForeignKey

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(Float, primary_key=True, default=lambda: secrets.randbelow(1_000_000_000))
    name = db.Column(String(100),  unique=True)
    password = db.Column(String(100))
    city = db.Column(String(100))
    role = db.Column(String(100),  default='customer')
    email = db.Column(String(100),)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def __repr__(self):
        return f'<Customer {self.name}>'



class Professional(db.Model):
    __tablename__ = 'professionals'

    id = db.Column(Float, primary_key=True, default=lambda: secrets.randbelow(1_000_000_000))
    name = db.Column(String(100),    unique=True)
    service = db.Column(String(100),  )
    password = db.Column(String(1000))
    city = db.Column(String(100) )
    experience = db.Column(Integer,  )
    approval = db.Column(String(100),  )
    rating = db.Column(Float, nullable=True)
    role = db.Column(String(100),  default='professional')
    email = db.Column(String(100),  )
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def __repr__(self):
        return f'<Professional {self.name}>'

class Work(db.Model):
    __tablename__ = 'works'

    id = db.Column(Float, primary_key=True,default=lambda: secrets.randbelow(1_000_000_000))
    name = db.Column(String(100),unique=True)
    description = db.Column(String(255),  )
    amount = db.Column(Float,  )
    date = db.Column(Date, default=datetime.utcnow)
    service = db.Column(String(100),  )
    address = db.Column(String(255),  )
    status = db.Column(String(50), default ='open')
    customer_id = db.Column(Float,  )
    professional_id = db.Column(Float,  )
    rating = db.Column(Float, nullable=True)
    city = db.Column(String(100),  )

    def __repr__(self):
        return f'<Work {self.name} - {self.status}>'

class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(Float, primary_key=True, default=lambda: secrets.randbelow(1_000_000_000))
    work_name = db.Column(String(100),  )
    source = db.Column(Float,  )
    target = db.Column(Float,  )
    od_amount = db.Column(Float,  )
    status = db.Column(String(50),  default='pending')
    od_date = db.Column(Date, default=datetime.utcnow)
    cr_date = db.Column(Date, default=datetime.utcnow)


    def __repr__(self):
        return f'<Offer {self.id} from {self.source} to {self.target}>'

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(Float, primary_key=True, default=lambda: secrets.randbelow(1_000_000_000))
    service = db.Column(String(100),unique=True )
    base = db.Column(Float,  )

    def __repr__(self):
        return f'<Service {self.service}>'

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(Float, primary_key=True, default=lambda: secrets.randbelow(1_000_000_000))
    city = db.Column(String(100),unique=True )
    state = db.Column(String(100),  )

    def __repr__(self):
        return f'<Location {self.city}, {self.state}>'

def make_data():
    if not Customer.query.filter_by(name='admin').first():
        db.session.add(Customer(name='admin', role='admin', password= generate_password_hash('admin'), city='Hyderabad'))
        db.session.add(Customer(name='cust1', email='cust1@gmail.com', password= generate_password_hash('8888'), city='Hyderabad'))
        db.session.add(Customer(name='cust2', password= generate_password_hash('8888'), city='Hyderabad', email='cust2@gmail.com'))
        db.session.add(Professional(name='prof1', service='AC Repair', password= generate_password_hash('8888'), city='Hyderabad',approval="T"))
        db.session.add(Professional(name='prof2', service='AC Repair', password= generate_password_hash('8888'), city='Hyderabad',approval="T"))
        db.session.add(Location(city='Hyderabad', state='Telangana'))
        db.session.add(Service(service='AC Repair', base=2000))
        db.session.commit()
        cust1 = Customer.query.filter_by(name='cust1').first()
        cust2 = Customer.query.filter_by(name='cust2').first()
        prof1 = Professional.query.filter_by(name='prof1').first()
        prof2 = Professional.query.filter_by(name='prof2').first()
        db.session.add(Work(name='work1', description='Work1', amount=1000, customer_id=cust1.id, date=datetime.now(),service='AC Repair',address='near rock', city='Hyderabad'))
        db.session.add(Work(name='work2', description='Work2', amount=1000, customer_id=cust2.id, date=datetime.now(),service='AC Repair',address='near rock', city='Hyderabad',status='closed'))
        db.session.add(Offer(work_name='work1', source=prof1.id,target=cust1.id,od_amount=1100,status='pending',od_date=datetime.now()))
        db.session.add(Offer(work_name='work2', source=prof2.id,target=cust2.id,od_amount=1100,status='accepted',od_date=datetime.now()))
        db.session.add(Offer(work_name='work1', source=cust1.id,target=prof1.id,od_amount=1050,status='pending',od_date=datetime.now()))
        db.session.commit()