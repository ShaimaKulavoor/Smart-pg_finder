#!/usr/bin/env python
"""
DEBUG SCRIPT - Initialize Database and Test Endpoints
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("\n" + "=" * 80)
print("🔧 SMART PG FINDER - DATABASE INITIALIZATION & API TEST")
print("=" * 80)

# Step 1: Initialize Flask app and database
print("\n1️⃣ Initializing Flask app and database...")
try:
    os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))
    sys.path.insert(0, os.getcwd())
    
    from app import app, db
    from models import User, PG
    from load_data import load_data_to_db
    
    with app.app_context():
        print("   ✅ Flask app initialized")
        
        # Create all tables
        db.create_all()
        print("   ✅ Database tables created")
        
        # Check if data already exists
        existing_count = PG.query.count()
        print(f"   📊 Existing PGs in database: {existing_count}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 2: Load CSV data
print("\n2️⃣ Loading CSV data into database...")
try:
    csv_path = '../data/House_Rent_Dataset.csv'
    
    with app.app_context():
        existing = PG.query.count()
        if existing > 0:
            print(f"   ⚠️  Database already has {existing} PGs")
            print("   Skipping data load (database already populated)")
        else:
            print(f"   Loading from: {csv_path}")
            load_data_to_db(csv_path, app)
            
            # Verify load
            total = PG.query.count()
            print(f"   ✅ Loaded {total} PGs into database")
            
            # Get cities
            cities = db.session.query(PG.city).distinct().all()
            cities = [c[0] for c in cities if c[0]]
            print(f"   📍 Cities in database: {len(cities)} unique cities")
            print(f"      Examples: {', '.join(cities[:5])}")
            
except Exception as e:
    print(f"   ❌ Error loading data: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 3: Test basic queries
print("\n3️⃣ Testing database queries...")
try:
    with app.app_context():
        # Test 1: Get all cities
        cities = db.session.query(PG.city).distinct().all()
        cities = [c[0] for c in cities if c[0]]
        print(f"   ✅ Cities query: {len(cities)} cities found")
        
        # Test 2: Filter by city
        kolkata_pgs = PG.query.filter(PG.city == 'Kolkata').count()
        print(f"   ✅ Kolkata filter: {kolkata_pgs} PGs in Kolkata")
        
        # Test 3: Filter by budget
        budget_pgs = PG.query.filter(PG.rent <= 10000).count()
        print(f"   ✅ Budget filter: {budget_pgs} PGs under ₹10,000")
        
        # Test 4: Combined filter
        result = PG.query.filter(
            (PG.city == 'Kolkata') & 
            (PG.rent <= 15000)
        ).limit(5).all()
        print(f"   ✅ Combined filter: Found {len(result)} PGs")
        if result:
            pg = result[0]
            print(f"      Sample: {pg.area_locality}, {pg.city} - ₹{pg.rent}/mo ({pg.bhk} BHK)")
        
except Exception as e:
    print(f"   ❌ Error in queries: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 4: Database summary
print("\n4️⃣ Database summary...")
try:
    with app.app_context():
        total_pgs = PG.query.count()
        total_users = User.query.count()
        avg_rent = db.session.query(db.func.avg(PG.rent)).scalar()
        
        print(f"   📊 Total PGs: {total_pgs}")
        print(f"   👥 Total Users: {total_users}")
        print(f"   💰 Average rent: ₹{avg_rent:.0f}/mo")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
print("✅ DATABASE INITIALIZATION COMPLETE")
print("=" * 80)

print("\n📝 NEXT STEPS:")
print("   1. Start backend: python backend/app.py")
print("   2. Test endpoints:")
print("      - GET http://localhost:5000/api/health")
print("      - GET http://localhost:5000/api/cities")
print("      - GET http://localhost:5000/api/recommend?city=Kolkata&max_budget=15000")
print("   3. Start frontend: cd frontend && npm start")

print("\n" + "=" * 80)
