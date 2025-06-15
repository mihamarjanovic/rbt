from flask import Blueprint, request
from . import db
from .models import Building, EstateType, CityPart, City, State

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    return 'Real Estate API'

@bp.route('/test-db')
def test_db():
    count = db.session.query(Building).count()
    return f'Total buildings: {count}'

@bp.route('/properties/<int:id>')
def get_property(id):
    building = Building.query.get_or_404(id)
    return {
        'id': building.id,
        'square_footage': float(building.square_footage) if building.square_footage is not None else None,
        'construction_year': building.construction_year,
        'price': building.price,
        'rooms': float(building.rooms) if building.rooms is not None else None,
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

    properties = query.all()

    return [{
        'id': building.id,
        'square_footage': float(building.square_footage) if building.square_footage is not None else None,
        'construction_year': building.construction_year,
        'price': building.price,
        'rooms': float(building.rooms) if building.rooms is not None else None,
        'bathrooms': building.bathrooms,
        'parking': building.parking,
        'estate_type': building.estate_type.name,
        'offer': building.offer.name,
        'city_part': building.city_part.name if building.city_part else None
    } for building in properties]