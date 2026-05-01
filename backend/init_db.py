"""
Database initialization script
Run this to load CSV data into SQLite database
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app        # ✅ import app from app.py
from extensions import db  # ✅ import db from extensions.py
from load_data import load_data_to_db

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  SMART PG FINDER - DATABASE INITIALIZATION")
    print("="*60 + "\n")
    
    # Get CSV path
    csv_path = input("Enter path to CSV file (default: ../data/House_Rent_Dataset.csv): ").strip()
    if not csv_path:
        csv_path = '../data/House_Rent_Dataset.csv'
    
    # ✅ CREATE TABLES FIRST
    with app.app_context():
        print("📦 Creating database tables...")
        db.create_all()
    
    # Load data
    load_data_to_db(csv_path, app)
    
    print("\n" + "="*60)
    print("✅ Database initialization complete!")
    print("="*60 + "\n")