
# Import libraries
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import time
db = SQLAlchemy()
from sqlalchemy import create_engine,func

from datetime import datetime
from sqlalchemy import Float, Integer, String, Date, ForeignKey

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(Float, primary_key=True, default=time.time())
    name = db.Column(String(100),  unique=True)
    password = db.Column(String(100))
    city = db.Column(String(100))
    role = db.Column(String(100),  default='customer')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def __repr__(self):
        return f'<Customer {self.name}>'



class Professional(db.Model):
    __tablename__ = 'professionals'

    id = db.Column(Float, primary_key=True)
    name = db.Column(String(100),    unique=True)
    service = db.Column(String(100),  )
    password = db.Column(String(1000))
    city = db.Column(String(100) )
    experience = db.Column(Integer,  )
    approval = db.Column(String(100),  )
    rating = db.Column(Float, nullable=True)
    role = db.Column(String(100),  default='professional')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def __repr__(self):
        return f'<Professional {self.name}>'

class Work(db.Model):
    __tablename__ = 'works'

    id = db.Column(Float, primary_key=True,default=time.time())
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

    id = db.Column(Float, primary_key=True, default=time.time())    
    work_id = db.Column(Float, ForeignKey('works.id'),  )
    source = db.Column(Float,  )
    target = db.Column(Float,  )
    amount = db.Column(Float,  )
    status = db.Column(String(50),  )
    od_date = db.Column(Date, default=datetime.utcnow)
    cr_date = db.Column(Date, default=datetime.utcnow)

    # Relationship for work
    work = db.relationship('Work', backref=db.backref('offers', lazy=True))

    def __repr__(self):
        return f'<Offer {self.id} from {self.source} to {self.target}>'

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(Float, primary_key=True, default=time.time())
    service = db.Column(String(100),  )
    base = db.Column(Float,  )

    def __repr__(self):
        return f'<Service {self.service}>'

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(Float, primary_key=True, default=time.time())
    city = db.Column(String(100),  )
    state = db.Column(String(100),  )

    def __repr__(self):
        return f'<Location {self.city}, {self.state}>'

def make_data():
    if not Customer.query.filter_by(name='admin').first():
        db.session.add(Customer(name='admin', role='admin', password= generate_password_hash('admin'), city='Hyderabad', id=time.time()))
        time.sleep(0.1)
        db.session.add(Location(city='Hyderabad', state='Telangana', id=time.time()))
        time.sleep(0.1)
        db.session.add(Service(service='AC Repair', base=2000, id=time.time()))
        time.sleep(0.1)
        db.session.commit()