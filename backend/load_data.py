"""
Data loading script for Smart PG Recommendation App
Loads CSV data into SQLite database
"""

import pandas as pd
import sys
import os
import random

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

def load_data_to_db(csv_path, app):
    """
    Load house rental data from CSV into database
    
    Args:
        csv_path: Path to the CSV file
        app: Flask application instance
    """
    try:
        print("📁 Loading data from CSV...")
        df = pd.read_csv(csv_path)
        print(f"✓ Loaded {len(df)} records from CSV")
        
        print(f"Columns found: {', '.join(df.columns)}")
        
        with app.app_context():
            from models import PG, Amenity
            from app import db
            
            # Check if data already exists
            existing_count = PG.query.count()
            if existing_count > 0:
                print(f"\n⚠️  Database already contains {existing_count} PGs.")
                response = input("Clear existing data and reload? (yes/no): ")
                if response.lower() == 'yes':
                    db.session.query(PG).delete()
                    db.session.commit()
                else:
                    print("Keeping existing data.")
                    return
            
            # Process and load data
            print("\n🔄 Processing data...")
            
            # Define default amenities
            default_amenities = [
                ('High-speed WiFi', True),
                ('Parking', True),
                ('Meals Included', True),
                ('Laundry Service', False),
                ('Air Conditioning', False)
            ]
            
            # List of placeholder images
            placeholder_images = [
                '/images/pg/pg_placeholder_1.svg',
                '/images/pg/pg_placeholder_2.svg',
                '/images/pg/pg_placeholder_3.svg',
                '/images/pg/pg_placeholder_4.svg',
                '/images/pg/pg_placeholder_5.svg'
            ]
            
            # Load data row by row
            for idx, row in df.iterrows():
                try:
                    # Generate mock owner details
                    owner_names = ['Rajesh Kumar', 'Priya Singh', 'Amit Patel', 'Neha Sharma', 
                                  'Vikram Reddy', 'Deepak Gupta', 'Sandhya Verma', 'Arjun Nair']
                    owner_name = random.choice(owner_names)
                    owner_phone = f"+91-{random.randint(8000000000, 9999999999)}"
                    owner_email = f"owner{random.randint(1, 9999)}@pgfinder.com"
                    
                    pg = PG(
                        posted_on=str(row.get('Posted On', '2022-01-01')),
                        bhk=int(row.get('BHK', 1)) if pd.notna(row.get('BHK')) else 1,
                        rent=int(row.get('Rent', 0)) if pd.notna(row.get('Rent')) else 0,
                        size=int(row.get('Size', 0)) if pd.notna(row.get('Size')) else 0,
                        floor=str(row.get('Floor', 'Ground')),
                        area_type=str(row.get('Area Type', 'Super Area')),
                        area_locality=str(row.get('Area Locality', 'Unknown')),
                        city=str(row.get('City', 'Unknown')),
                        furnishing_status=str(row.get('Furnishing Status', 'Unfurnished')),
                        tenant_preferred=str(row.get('Tenant Preferred', 'Any')),
                        bathroom=int(row.get('Bathroom', 1)) if pd.notna(row.get('Bathroom')) else 1,
                        point_of_contact=str(row.get('Point of Contact', 'Contact Owner')),
                        rating=4.0,  # Default rating
                        image_url=random.choice(placeholder_images),  # Random placeholder image
                        description=f"{row.get('BHK', 1)} BHK in {row.get('Area Locality', 'Unknown')}, {row.get('City', 'Unknown')}",
                        # Owner details
                        owner_name=owner_name,
                        owner_phone=owner_phone,
                        owner_email=owner_email
                    )
                    
                    db.session.add(pg)
                    
                    # Add amenities periodically
                    if (idx + 1) % 100 == 0:
                        db.session.flush()
                        print(f"  Processed {idx + 1} records...")
                
                except Exception as e:
                    print(f"  ⚠️  Error processing row {idx}: {str(e)}")
                    continue
            
            # Commit all changes
            print("\n💾 Saving to database...")
            db.session.commit()
            
            # Add amenities to all PGs
            print("📝 Adding amenities...")
            all_pgs = PG.query.all()
            for pg in all_pgs:
                for amenity_name, available in default_amenities:
                    amenity = Amenity(
                        pg_id=pg.id,
                        name=amenity_name,
                        available=available
                    )
                    db.session.add(amenity)
            
            db.session.commit()
            
            final_count = PG.query.count()
            print(f"\n✓ Successfully loaded {final_count} PGs into database!")
            print("✓ Database initialization complete!")
            
    except FileNotFoundError:
        print(f"❌ Error: CSV file not found at {csv_path}")
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")

if __name__ == '__main__':
    # This will be run during setup
    pass
