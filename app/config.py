import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://real_estate_user:real_estate_password@localhost/real_estate')
    SQLALCHEMY_TRACK_MODIFICATIONS = False