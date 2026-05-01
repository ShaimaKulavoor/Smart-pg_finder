#!/usr/bin/env python
"""Quick API endpoint test"""
import sys
sys.path.insert(0, 'backend')

import requests

print("\n" + "="*60)
print("🧪 TESTING BACKEND API ENDPOINTS")
print("="*60)

# Test 1: Health
print("\n1️⃣ Testing /health endpoint...")
try:
    r = requests.get('http://localhost:5000/health')
    print(f"   ✅ Status: {r.status_code}")
    print(f"   Response: {r.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Cities
print("\n2️⃣ Testing /api/cities endpoint...")
try:
    r = requests.get('http://localhost:5000/api/cities')
    data = r.json()
    print(f"   ✅ Status: {r.status_code}")
    print(f"   Cities: {len(data['cities'])} - {', '.join(data['cities'][:3])}...")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Recommendations
print("\n3️⃣ Testing /api/recommend endpoint...")
try:
    r = requests.get('http://localhost:5000/api/recommend?city=Kolkata&max_budget=15000')
    data = r.json()
    recs = data.get('recommendations', [])
    print(f"   ✅ Status: {r.status_code}")
    print(f"   Found: {len(recs)} recommendations")
    if recs:
        rec = recs[0]
        print(f"   Sample: {rec['area_locality']}, {rec['city']} - ₹{rec['rent']}/mo ({rec['bhk']} BHK)")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("✅ API TESTING COMPLETE")
print("="*60)
