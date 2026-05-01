#!/usr/bin/env python
"""
SMART PG FINDER - Complete Setup & Debug Script
Run this FIRST before running the app
"""

import os
import sys
import subprocess

print("\n" + "=" * 70)
print("🚀 SMART PG FINDER - SETUP & DEBUG SCRIPT")
print("=" * 70)

# Step 1: Check Python
print("\n1️⃣ Checking Python installation...")
print(f"   Python: {sys.executable}")
print(f"   Version: {sys.version}")

# Step 2: Create venv if not exists
venv_path = '.venv'
print(f"\n2️⃣ Checking virtual environment...")
if not os.path.exists(venv_path):
    print(f"   Creating virtual environment at {venv_path}...")
    subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)
    print(f"   ✅ Virtual environment created")
else:
    print(f"   ✅ Virtual environment already exists")

# Step 3: Install backend requirements
print(f"\n3️⃣ Installing backend dependencies...")
backend_req = os.path.join('backend', 'requirements.txt')
if os.path.exists(backend_req):
    pip_exe = os.path.join(venv_path, 'Scripts', 'pip')
    subprocess.run([pip_exe, 'install', '-r', backend_req, '-q'], check=True)
    print(f"   ✅ Backend dependencies installed")
else:
    print(f"   ❌ {backend_req} not found")

# Step 4: Check dataset
print(f"\n4️⃣ Checking dataset...")
csv_path = 'data/House_Rent_Dataset.csv'
if os.path.exists(csv_path):
    size_mb = os.path.getsize(csv_path) / (1024 * 1024)
    print(f"   ✅ Dataset found: {csv_path} ({size_mb:.2f} MB)")
else:
    print(f"   ❌ Dataset NOT found at {csv_path}")
    print(f"   Please place House_Rent_Dataset.csv in the data/ folder")

# Step 5: Load and inspect dataset
print(f"\n5️⃣ Inspecting dataset...")
try:
    python_exe = os.path.join(venv_path, 'Scripts', 'python')
    
    inspect_code = """
import pandas as pd
import sys

try:
    df = pd.read_csv('data/House_Rent_Dataset.csv')
    print(f"   ✅ Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"\\n   COLUMNS (actual from CSV):")
    for i, col in enumerate(df.columns, 1):
        print(f"      {i}. {col}")
    print(f"\\n   SAMPLE DATA (first row):")
    for col in df.columns[:5]:
        val = df[col].iloc[0]
        print(f"      {col}: {val}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)
"""
    
    result = subprocess.run(
        [python_exe, '-c', inspect_code],
        capture_output=True,
        text=True,
        cwd='.'
    )
    print(result.stdout)
    if result.stderr:
        print(f"   Error: {result.stderr}")

except Exception as e:
    print(f"   ⚠️  Could not inspect dataset: {e}")

print("\n" + "=" * 70)
print("✅ SETUP COMPLETE")
print("=" * 70)

print("\n📝 NEXT STEPS:")
print("   1. Activate venv: .venv\\Scripts\\Activate.ps1")
print("   2. Run database setup: python backend/init_db.py")
print("   3. Start backend: python backend/app.py")
print("   4. (In new terminal) Start frontend: cd frontend && npm install && npm start")

print("\n" + "=" * 70)
