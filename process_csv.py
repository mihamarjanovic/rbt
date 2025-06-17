import os
import pandas as pd
import time
from sqlalchemy.exc import IntegrityError
from app import db, create_app
from app.models import Building, EstateType, Offer, CityPart

app = create_app()

def process_csv(file_path):
    with app.app_context():
        try:
            df = pd.read_csv(file_path)
            df = df[df['status'] == 'for_sale']

            estate_type = EstateType.query.filter_by(name='kuća').first()
            offer = Offer.query.filter_by(name='Prodaja').first()
            city_part = CityPart.query.first()

            if not all([estate_type, offer, city_part]):
                raise ValueError("Missing required database entries (kuća, prodaja, or city part)")

            for _, row in df.iterrows():
                price_eur = int(row['price'] * 0.92) if pd.notnull(row['price']) else None
                square_meters = row['house_size'] * 0.092903 if pd.notnull(row['house_size']) else None
                land_area_m2 = row['acre_lot'] * 4047 if pd.notnull(row['acre_lot']) else None

                building = Building(
                    square_footage=square_meters,
                    price=price_eur,
                    rooms=row['bed'] if pd.notnull(row['bed']) else None,
                    bathrooms=row['bath'] if pd.notnull(row['bath']) else None,
                    land_area=land_area_m2,
                    estate_type_id=estate_type.id,
                    offer_id=offer.id,
                    city_part_id=city_part.id,
                    registration=False,
                    parking=False,
                    construction_year=None
                )
                db.session.add(building)
            db.session.commit()
            os.rename(file_path, os.path.join('processed', os.path.basename(file_path)))
            print(f"Processed: {file_path}")
        except (IntegrityError, AttributeError, KeyError, pd.errors.ParserError, ValueError) as e:
            db.session.rollback()
            os.rename(file_path, os.path.join('errored', os.path.basename(file_path)))
            print(f"Error processing {file_path}: {str(e)}")

def monitor_directory():
    staging_dir = 'staging'
    while True:
        for filename in os.listdir(staging_dir):
            if filename.endswith('.csv'):
                process_csv(os.path.join(staging_dir, filename))
        time.sleep(300)

if __name__ == "__main__":
    monitor_directory()