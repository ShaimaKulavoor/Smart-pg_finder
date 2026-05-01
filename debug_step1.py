#!/usr/bin/env python
"""
DEBUG SCRIPT - Step 1: Check Dataset and Backend Setup
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 70)
print("SMART PG FINDER - DEBUG SCRIPT")
print("=" * 70)

# Step 1: Check if CSV exists
csv_path = 'data/House_Rent_Dataset.csv'
print(f"\n1️⃣ Checking CSV file: {csv_path}")
if not os.path.exists(csv_path):
    print(f"❌ CSV NOT FOUND at {csv_path}")
    sys.exit(1)
else:
    print(f"✅ CSV found at {csv_path}")

# Step 2: Load CSV and inspect
try:
    import pandas as pd
    print("\n2️⃣ Loading CSV with pandas...")
    df = pd.read_csv(csv_path)
    print(f"✅ CSV loaded successfully")
    print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    print(f"\n3️⃣ Column names (ACTUAL):")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. '{col}'")
    
    print(f"\n4️⃣ Data types:")
    for col, dtype in zip(df.columns, df.dtypes):
        print(f"   {col}: {dtype}")
    
    print(f"\n5️⃣ First 2 rows:")
    print(df.head(2).to_string())
    
    # Check for required columns
    required_cols = ['city', 'rent', 'bhk', 'area_locality', 'furnishing_status', 'tenant_preferred']
    print(f"\n6️⃣ Checking for required columns:")
    df_cols_lower = [col.lower().replace(' ', '_') for col in df.columns]
    for col in required_cols:
        if col in df_cols_lower:
            print(f"   ✅ '{col}' found")
        else:
            print(f"   ❌ '{col}' NOT FOUND")
            print(f"   Available: {df_cols_lower}")
    
    # Check data
    print(f"\n7️⃣ Data quality:")
    print(f"   Missing values: {df.isnull().sum().sum()}")
    print(f"   Unique cities: {df['City'].nunique() if 'City' in df.columns else 'N/A'}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Run: pip install -r backend/requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error loading CSV: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ DEBUG STEP 1 COMPLETE")
print("=" * 70)
