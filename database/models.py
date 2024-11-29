
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

class MetaData(db.Model):
    __tablename__ = 'metadata'

    id = db.Column(Float, primary_key=True, default=lambda: secrets.randbelow(1_000_000_000))
    dtype = db.Column(String(100) )
    name = db.Column(String(100),  )
    info = db.Column(String(100),  )

    def __repr__(self):
        return f'<metaData {self.dtype}>'

def my_work(cust_id):
    sent_offers_data=None;rec_data=None;rec_data=None;hist_data=None;actw=None;act_data=None
    try:
        sent_offers=Offer.query.filter_by(source=cust_id,status='pending').all()
        sent_offers_data = [{'offer id':sent_offer.id,'work_name':sent_offer.work_name,'amount':sent_offer.od_amount,'date':sent_offer.od_date
                             ,'professional':get_professional(Professional.query.filter_by(id=sent_offer.target).first().id)
                             } for sent_offer in sent_offers] 
    except Exception as e:
        print(f"Error: {str(e)}")
    try:
        
        rec_offers=Offer.query.filter_by(target=cust_id,status='pending').all()
        rec_data=[{'offer id':rec.id,'work_name':rec.work_name,'amount':rec.od_amount,'date':rec.od_date
                             ,'professional':get_professional(Professional.query.filter_by(id=rec.source).first().id)
                              
                             } for rec in rec_offers] 
    except Exception as e:
        print(f"Error: {str(e)}")
    try:
        hist= Offer.query.filter(or_(Offer.source == cust_id, Offer.target ==cust_id),Offer.status.in_(['rejected', 'accepted'])).all()
        hist_data=   [{'offer id':histo.id,'work_name':histo.work_name,'amount':histo.od_amount,'date':histo.od_date
                             ,'professional':get_professional(Professional.query.filter_by(id=histo.target).first().id) if Customer.query.filter_by(id=histo.source).first() else get_professional(Professional.query.filter_by(id=histo.source).first().id)
        ,'rating':Work.query.filter_by(name=histo.work_name).first().rating  if histo.status=='accepted' else 'rejected'
        } for histo in hist]
    except Exception as e:
        print(f"Error: {str(e)}")
    try:
        actw=Offer.query.filter(or_(Offer.source == cust_id, Offer.target ==cust_id),Offer.status.in_(['accepted'])).all()
        act_data=[{'offer id':act.id,'work_name':act.work_name,'amount':act.od_amount,'date':act.od_date
                             ,'professional':get_professional(Professional.query.filter_by(id=act.target).first().id) if Customer.query.filter_by(id=act.source).first() else get_professional(Professional.query.filter_by(id=act.source).first().id),
                             } for act in actw] 
    except Exception as e:
        print(f"Error: {str(e)}")
    try:
        response={'sent':sent_offers_data if sent_offers_data else [],'received':rec_data if rec_data else [],'active':act_data if act_data else [],'history':hist_data if hist_data else []}
        return jsonify(response), 200  # Return JSON response
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500 
    
def your_works(prof_id):
    sent_offers_data=None;rec_data=None;rec_data=None;hist_data=None;actw=None;act_data=None
    try:
        sent_offers=Offer.query.filter_by(source=prof_id,status='pending').all()
        sent_offers_data = [{'offer id':sent_offer.id,'work_name':sent_offer.work_name,'amount':sent_offer.od_amount,'date':sent_offer.od_date
                             ,'customer':get_customer(Customer.query.filter_by(id=sent_offer.target).first().id)
                             } for sent_offer in sent_offers] 
    except Exception as e:
        print(f"Error: {str(e)}")
    try:
        rec_offers=Offer.query.filter_by(target=prof_id,status='pending').all()
        rec_data=[{'offer id':rec.id,'work_name':rec.work_name,'amount':rec.od_amount,'date':rec.od_date
                             ,'customer':get_customer(Customer.query.filter_by(id=rec.source).first().id)
                             } for rec in rec_offers] 
    except Exception as e:
        print(f"Error: {str(e)}")
    try:
        hist= Offer.query.filter(or_(Offer.source == prof_id, Offer.target ==prof_id),Offer.status.in_(['rejected', 'accepted'])).all()
        hist_data=   [{'offer id':histo.id,'work_name':histo.work_name,'amount':histo.od_amount,'date':histo.od_date
                             ,'customer':get_customer(Customer.query.filter_by(id=histo.source).first().id) if Customer.query.filter_by(id=histo.source).first() else get_customer(Customer.query.filter_by(id=histo.target).first().id),
                             'rating':Work.query.filter_by(name=histo.work_name).first().rating if histo.status=='accepted' else 'rejected'
                             } for histo in hist]
    except Exception as e:
        print(f"Error: {str(e)}")
    try:
        actw=Offer.query.filter(or_(Offer.source == prof_id, Offer.target ==prof_id),Offer.status.in_(['accepted'])).all()
        act_data=[{'offer id':act.id,'work_name':act.work_name,'amount':act.od_amount,'date':act.od_date
                             ,'customer':get_customer(Customer.query.filter_by(id=act.source).first().id) if Customer.query.filter_by(id=act.source).first() else get_customer(Customer.query.filter_by(id=act.target).first().id)} for act in actw]
    except Exception as e:
        print(f"Error: {str(e)}")
    try:
        data={'sent':sent_offers_data if sent_offers_data else [],'received':rec_data if rec_data else [],'active':act_data if act_data else [],'history':hist_data if hist_data else []}
        return jsonify(data),200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500  
    
def discover_works(prof_id): #v
    try:
        Profes=Professional.query.filter_by(id=prof_id).first()
        worksz = Work.query.filter_by(service=Profes.service,status='open').all()
        works_data = [{ 'name': work.name, 'description': work.description, 'amount': work.amount, 
                        'date': work.date, 'address': work.address, 
                        'customer':get_customer(Customer.query.filter_by(id=work.customer_id).first().id),
                            'city': work.city} for work in worksz]
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
    return jsonify(works_data),200


#use id to get key values
def get_professional(professional_id):
    try:
        professional = Professional.query.get(professional_id)
        if professional:
            # Return the data as a dictionary, not as a Flask response
            return {
                'id': professional.id,
                'name': professional.name,
                'email': professional.email,
                'service': professional.service,
                'experience': professional.experience,
                'approval': professional.approval,
                'rating': professional.rating,
                'city': professional.city
            }
        else:
            return None
    except Exception as e:
        return {"error": str(e)}

def get_customer(customer_id):
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
            return customer_data
        else:
            return None
    except Exception as e:
        return {"error": str(e)}

#admin usage
def get_professionals_data():
    # Query for approved and unapproved professionals
    profs = Professional.query.filter_by(approval='T').all()
    uprofs = Professional.query.filter_by(approval='F').all()

    # Create data dictionaries using list comprehension
    appro_data = [get_professional(profi.id) for profi in profs]
    uappro_data = [get_professional(profi.id) for profi in uprofs]

    # Filter out None values in case get_professional_json returned None for any professional
    appro_data = [data for data in appro_data if data is not None]
    uappro_data = [data for data in uappro_data if data is not None]

    # Combine the data into a single dictionary
    prof_data = {
        'approved': appro_data,
        'unapproved': uappro_data
    }

    # Return the JSON response
    return jsonify(prof_data), 200


# Function to get all types of works  for a given customer_id
def new_work(cust_id): #v
    try:
        # Query all works for the given customer_id
        open_works = Work.query.filter_by(customer_id=cust_id,status='open').all()
        open_works_data = [{'id': open_work.id, 'name': open_work.name, 'description': open_work.description, 'amount': open_work.amount, 
                       'date': open_work.date, 'service': open_work.service, 'address': open_work.address, 
                         'city': open_work.city} for open_work in open_works]
        done_works = Work.query.filter_by(customer_id=cust_id,status='done').all()
        done_works_data = [{'id': done_work.id, 'name': done_work.name, 'description': done_work.description, 'amount': done_work.amount, 
                       'date': done_work.date, 'service': done_work.service, 'address': done_work.address, 
                        'rating': done_work.rating, 'city': done_work.city} for done_work in done_works]
        closed_works = Work.query.filter_by(customer_id=cust_id,status='closed').all()
        closed_works_data = [{'id': closed_work.id, 'name': closed_work.name, 'description': closed_work.description, 'amount': closed_work.amount, 
                       'date': closed_work.date, 'service': closed_work.service, 'address': closed_work.address, 
                         'city': closed_work.city} for closed_work in closed_works]
        response_data = {'open_works': open_works_data, 'done_works': done_works_data, 'closed_works': closed_works_data}   
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500  # Handle any errors



def make_data():
    if not Customer.query.filter_by(name='admin').first():
        db.session.add(Customer(name='admin', role='admin', password= generate_password_hash('admin'), city='Hyderabad'))
        db.session.add(Customer(name='cust1', email='cust1@gmail.com', password= generate_password_hash('8888'), city='Hyderabad'))
        db.session.add(Customer(name='cust2', password= generate_password_hash('8888'), city='Hyderabad', email='cust2@gmail.com'))
        db.session.add(Professional(name='prof1', service='AC Repair', password= generate_password_hash('8888'), city='Hyderabad',approval="T",email='prof1@gmail.com'))
        db.session.add(Professional(name='prof2', service='AC Repair', password= generate_password_hash('8888'), city='Hyderabad',approval="T",email='prof2@gmail.com'))
        db.session.add(MetaData(name='Hyderabad', info='Telangana',dtype='city'))
        db.session.add(MetaData(name='AC Repair', info=2000,dtype='service'))
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