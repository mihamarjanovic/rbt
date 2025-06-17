from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from . import db
from .models import Building, EstateType, CityPart, City, State, Offer, User
from sqlalchemy.exc import IntegrityError

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    return 'Real Estate API'

@bp.route('/test-db')
def test_db():
    count = db.session.query(Building).count()
    return f'Total buildings: {count}'

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token}), 200

@bp.route('/properties/<int:id>')
def get_property(id):
    building = Building.query.get_or_404(id)
    return {
        'id': building.id,
        'square_footage': float(building.square_footage) if building.square_footage else None,
        'construction_year': building.construction_year,
        'price': building.price,
        'rooms': float(building.rooms) if building.rooms else None,
        'bathrooms': building.bathrooms,
        'parking': building.parking,
        'estate_type': building.estate_type.name,
        'offer': building.offer.name,
        'city_part': building.city_part.name if building.city_part else None
    }

@bp.route('/properties')
def search_properties():
    query = Building.query

    estate_type = request.args.get('estate_type')
    if estate_type:
        query = query.join(EstateType).filter(EstateType.name.ilike(estate_type))

    min_square_footage = request.args.get('min_square_footage', type=float)
    if min_square_footage:
        query = query.filter(Building.square_footage >= min_square_footage)

    max_square_footage = request.args.get('max_square_footage', type=float)
    if max_square_footage:
        query = query.filter(Building.square_footage <= max_square_footage)

    parking = request.args.get('parking', type=str)
    if parking and parking.lower() in ['yes', 'no']:
        query = query.filter(Building.parking == (parking.lower() == 'yes'))

    state = request.args.get('state')
    if state:
        query = query.join(CityPart).join(City).join(State).filter(State.name.ilike(state))

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    properties = pagination.items

    return {
        'properties': [{
            'id': building.id,
            'square_footage': float(building.square_footage) if building.square_footage else None,
            'construction_year': building.construction_year,
            'price': building.price,
            'rooms': float(building.rooms) if building.rooms else None,
            'bathrooms': building.bathrooms,
            'parking': building.parking,
            'estate_type': building.estate_type.name,
            'offer': building.offer.name,
            'city_part': building.city_part.name if building.city_part else None
        } for building in properties],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }

@bp.route('/properties', methods=['POST'])
@jwt_required()
def add_property():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = ['square_footage', 'construction_year', 'land_area', 'registration', 
                       'rooms', 'bathrooms', 'parking', 'price', 'estate_type_id', 
                       'offer_id', 'city_part_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        new_property = Building(
            square_footage=data['square_footage'],
            construction_year=data['construction_year'],
            land_area=data['land_area'],
            registration=data['registration'],
            rooms=data['rooms'],
            bathrooms=data['bathrooms'],
            parking=data['parking'],
            price=data['price'],
            estate_type_id=data['estate_type_id'],
            offer_id=data['offer_id'],
            city_part_id=data['city_part_id']
        )
        db.session.add(new_property)
        db.session.commit()
        return jsonify({
            'id': new_property.id,
            'square_footage': float(new_property.square_footage) if new_property.square_footage else None,
            'construction_year': new_property.construction_year,
            'land_area': float(new_property.land_area) if new_property.land_area else None,
            'registration': new_property.registration,
            'rooms': float(new_property.rooms) if new_property.rooms else None,
            'bathrooms': new_property.bathrooms,
            'parking': new_property.parking,
            'price': new_property.price,
            'estate_type': new_property.estate_type.name,
            'offer': new_property.offer.name,
            'city_part': new_property.city_part.name if new_property.city_part else None
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Invalid foreign key'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/properties/<int:id>', methods=['PUT'])
@jwt_required()
def update_property(id):
    building = Building.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        if 'square_footage' in data:
            building.square_footage = data['square_footage']
        if 'construction_year' in data:
            building.construction_year = data['construction_year']
        if 'land_area' in data:
            building.land_area = data['land_area']
        if 'registration' in data:
            building.registration = data['registration']
        if 'rooms' in data:
            building.rooms = data['rooms']
        if 'bathrooms' in data:
            building.bathrooms = data['bathrooms']
        if 'parking' in data:
            building.parking = data['parking']
        if 'price' in data:
            building.price = data['price']
        if 'estate_type_id' in data:
            building.estate_type_id = data['estate_type_id']
        if 'offer_id' in data:
            building.offer_id = data['offer_id']
        if 'city_part_id' in data:
            building.city_part_id = data['city_part_id']

        db.session.commit()
        return jsonify({
            'id': building.id,
            'square_footage': float(building.square_footage) if building.square_footage else None,
            'construction_year': building.construction_year,
            'land_area': float(building.land_area) if building.land_area else None,
            'registration': building.registration,
            'rooms': float(building.rooms) if building.rooms else None,
            'bathrooms': building.bathrooms,
            'parking': building.parking,
            'price': building.price,
            'estate_type': building.estate_type.name,
            'offer': building.offer.name,
            'city_part': building.city_part.name if building.city_part else None
        }), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Invalid foreign key'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500