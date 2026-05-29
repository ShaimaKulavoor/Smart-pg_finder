#!/usr/bin/env python
"""Test script to debug cities endpoint"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import app
from models import PG
from extensions import db

with app.app_context():
    print("Testing cities query...")
    
    # Test 1: Check PG count
    count = PG.query.count()
    print(f"✓ Total PGs in database: {count}")
    
    # Test 2: Query distinct cities
    cities_query = db.session.query(PG.city).distinct().all()
    print(f"✓ Raw query result: {cities_query[:5]}")
    
    # Test 3: Process cities
    cities = [city[0] for city in cities_query if city[0]]
    print(f"✓ Processed cities: {cities[:5]}")
    print(f"✓ Total cities: {len(cities)}")
    
    # Test 4: Make API request
    print("\nMaking API request...")
    with app.test_client() as client:
        response = client.get('/api/cities')
        print(f"Status: {response.status_code}")
        print(f"Data: {response.get_json()}")
