
# Import libraries
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, jsonify, request

from werkzeug.security import generate_password_hash, check_password_hash
import time
db = SQLAlchemy()
from sqlalchemy import create_engine,func
import secrets
from datetime import datetime
from sqlalchemy import Float, Integer, String, Date, ForeignKey,or_

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

def get_customer_json(customer_id):#v
    try:
        customer = Customer.query.filter_by(id=customer_id).first()  # Query Customer by ID
        if customer:
            # Create a dictionary of customer data without the password field
            customer_data = {
                'id': customer.id,
                'name': customer.name,
                'city': customer.city,
                'role': customer.role,
                'email': customer.email
            }
            return jsonify(customer_data), 200
        else:
            return jsonify({"message": "Customer not found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


def get_professional_json(professional_id):#v
    try:
        professional = Professional.query.filter_by(id=professional_id).first()  # Query Professional by ID
        if professional:
            # Create a dictionary of professional data without the password field
            professional_data = {
                'id': professional.id,
                'name': professional.name,
                'city': professional.city,
                'role': professional.role,
                'email': professional.email,
                'service': professional.service,
                'experience': professional.experience,
                'approval': professional.approval,
                'rating': professional.rating
            }
            return jsonify(professional_data), 200
        else:
            return jsonify({"message": "Professional not found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
from flask import jsonify

def my_work(cust_id):
    try:
        sent_offers=Offer.query.filter_by(source=cust_id,status='pending').all()
        sent_offers_data = [{'offer id':sent_offer.id,'work_name':sent_offer.work_name,'amount':sent_offer.od_amount,'date':sent_offer.od_date
                             ,'professional name':Professional.query.filter_by(id=sent_offer.target).first().name
                             ,'prefessional id':Professional.query.filter_by(id=sent_offer.target).first().id
                             } for sent_offer in sent_offers] 
        rec_offers=Offer.query.filter_by(target=cust_id,status='pending').all()
        rec_data=[{'offer id':rec.id,'work_name':rec.work_name,'amount':rec.od_amount,'date':rec.od_date
                             ,'professional name':Professional.query.filter_by(id=rec.source).first().name
                             ,'prefessional id':Professional.query.filter_by(id=rec.source).first().id
                             } for rec in rec_offers] 
        hist= Offer.query.filter(or_(Offer.source == cust_id, Offer.target ==cust_id),Offer.status.in_(['rejected', 'accepted'])).all()
        hist_data=   [{'offer id':histo.id,'work_name':histo.work_name,'amount':histo.od_amount,'date':histo.od_date
                             ,'professional name':Professional.query.filter_by(id=histo.target).first().name if Customer.query.filter_by(id=histo.source).first() else Professional.query.filter_by(id=histo.source).first().name
                             ,'prefessional id':Professional.query.filter_by(id=histo.target).first().id if Customer.query.filter_by(id=histo.source).first() else Professional.query.filter_by(id=histo.source).first().id,
        } for histo in hist]
        actw=Offer.query.filter(or_(Offer.source == cust_id, Offer.target ==cust_id),Offer.status.in_(['accepted'])).all()
        act_data=[{'offer id':act.id,'work_name':act.work_name,'amount':act.od_amount,'date':act.od_date
                             ,'professional name':Professional.query.filter_by(id=act.target).first().name if Customer.query.filter_by(id=act.source).first() else Professional.query.filter_by(id=act.source).first().name,
                             'prefessional id':Professional.query.filter_by(id=act.target).first().id if Customer.query.filter_by(id=act.source).first() else Professional.query.filter_by(id=act.source).first().id,
                             } for act in actw] 
                              
        response={'sent':sent_offers_data,'received':rec_data,'active':act_data,'history':hist_data}
        return jsonify(response), 200  # Return JSON response
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500 
    
def your_works(prof_id):
    try:
        sent_offers=Offer.query.filter_by(source=prof_id,status='pending').all()
        sent_offers_data = [{'offer id':sent_offer.id,'work_name':sent_offer.work_name,'amount':sent_offer.od_amount,'date':sent_offer.od_date
                             ,'customer name':Customer.query.filter_by(id=sent_offer.target).first().name
                             ,'customer id':Customer.query.filter_by(id=sent_offer.target).first().id
                             } for sent_offer in sent_offers] 
        rec_offers=Offer.query.filter_by(target=prof_id,status='pending').all()
        rec_data=[{'offer id':rec.id,'work_name':rec.work_name,'amount':rec.od_amount,'date':rec.od_date
                             ,'customer name':Customer.query.filter_by(id=rec.source).first().name
                             ,'customer id':Customer.query.filter_by(id=rec.source).first().id
                             } for rec in rec_offers] 
        hist= Offer.query.filter(or_(Offer.source == prof_id, Offer.target ==prof_id),Offer.status.in_(['rejected', 'accepted'])).all()
        hist_data=   [{'offer id':histo.id,'work_name':histo.work_name,'amount':histo.od_amount,'date':histo.od_date
                             ,'customer name':Customer.query.filter_by(id=histo.source).first().name if Customer.query.filter_by(id=histo.source).first() else Customer.query.filter_by(id=histo.target).first().name
                             ,'customer id':Customer.query.filter_by(id=histo.source).first().id if Customer.query.filter_by(id=histo.source).first() else Customer.query.filter_by(id=histo.target).first().id} for histo in hist]        
        actw=Offer.query.filter(or_(Offer.source == prof_id, Offer.target ==prof_id),Offer.status.in_(['accepted'])).all()
        act_data=[{'offer id':act.id,'work_name':act.work_name,'amount':act.od_amount,'date':act.od_date
                             ,'customer name':Customer.query.filter_by(id=act.source).first().name if Customer.query.filter_by(id=act.source).first() else Customer.query.filter_by(id=act.target).first().name
                             ,'customer id':Customer.query.filter_by(id=act.source).first().id if Customer.query.filter_by(id=act.source).first() else Customer.query.filter_by(id=act.target).first().id} for act in actw] 
        data={'sent':sent_offers_data,'received':rec_data,'active':act_data,'history':hist_data}
        return jsonify(data),200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500  
    
def discover_works(prof_id): #v
    try:
        Profes=Professional.query.filter_by(id=prof_id).first()
        worksz = Work.query.filter_by(service=Profes.service,status='open').all()
        works_data = [{ 'name': work.name, 'description': work.description, 'amount': work.amount, 
                        'date': work.date, 'address': work.address, 
                        'customer name':Customer.query.filter_by(id=work.customer_id).first().name,
                            'city': work.city} for work in worksz]
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
    return jsonify(works_data),200

# Function to get all works  for a given customer_id 
def new_work(cust_id): #v
    try:
        # Query all works for the given customer_id
        works = Work.query.filter_by(customer_id=cust_id).all()
        works_data = [{'id': work.id, 'name': work.name, 'description': work.description, 'amount': work.amount, 
                       'date': work.date, 'service': work.service, 'address': work.address, 
                       'status': work.status, 'rating': work.rating, 'city': work.city} for work in works]

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500  # Handle any errors
    
    return jsonify(works_data), 200  # Return JSON response
    '''
        # Query all offers where source or target matches the given user_id
        offers = Offer.query.filter((Offer.source == user_id) | (Offer.target == user_id)).all()
        offers_data = [{'id': offer.id, 'work_name': offer.work_name, 'source': offer.source, 'target': offer.target, 
                        'od_amount': offer.od_amount, 'status': offer.status, 'od_date': offer.od_date, 
                        'cr_date': offer.cr_date} for offer in offers]

        # Combine works and offers into a single JSON response
        response_data = {
            'works': works_data,
            'offers': offers_data
        }
'''



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
        db.session.add(Work(name='work2', description='Work2', amount=1000, customer_id=cust2.id, date=datetime.now(),service='AC Repair',address='near rock', city='Hyderabad'))
        db.session.add(Offer(work_name='work1', source=prof1.id,target=cust1.id,od_amount=1100,status='pending',od_date=datetime.now()))
        db.session.add(Offer(work_name='work1', source=prof2.id,target=cust1.id,od_amount=1100,status='pending',od_date=datetime.now()))
        db.session.add(Offer(work_name='work2', source=cust1.id,target=prof1.id,od_amount=1050,status='pending',od_date=datetime.now()))
        db.session.add(Offer(work_name='work2', source=cust1.id,target=prof1.id,od_amount=1050,status='pending',od_date=datetime.now()))
        db.session.commit()