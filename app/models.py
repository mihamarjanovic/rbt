from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Building(db.Model):
    __tablename__ = 'building'
    id = db.Column(db.Integer, primary_key=True)
    square_footage = db.Column(db.Float)
    construction_year = db.Column(db.Integer)
    land_area = db.Column(db.Float)
    registration = db.Column(db.Boolean)
    rooms = db.Column(db.Float)
    bathrooms = db.Column(db.Integer)
    parking = db.Column(db.Boolean)
    price = db.Column(db.Integer)
    estate_type_id = db.Column(db.Integer, db.ForeignKey('estate_type.id'), nullable=False)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)
    city_part_id = db.Column(db.Integer, db.ForeignKey('city_part.id'), nullable=False)
    estate_type = db.relationship('EstateType')
    offer = db.relationship('Offer')
    city_part = db.relationship('CityPart')

class EstateType(db.Model):
    __tablename__ = 'estate_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class CityPart(db.Model):
    __tablename__ = 'city_part'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    city = db.relationship('City')

class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    state = db.relationship('State')

class State(db.Model):
    __tablename__ = 'state'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))