from flask import Blueprint
from . import db
from .models import Building

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    return 'Real Estate API'

@bp.route('/test-db')
def test_db():
    count = db.session.query(Building).count()
    return f'Total buildings: {count}'