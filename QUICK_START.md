# 🚀 QUICK START GUIDE

## Prerequisites Check

Before you begin, ensure:
- ✅ Python 3.8+ installed (`python --version`)
- ✅ Node.js 14+ installed (`node --version`)
- ✅ CSV file copied to `data/House_Rent_Dataset.csv`

---

## 5-Minute Quick Start

### 1️⃣ Backend Setup (3 minutes)

**Open PowerShell and run:**

```powershell
# Navigate to backend
cd c:\smart_pg\backend

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
"FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=test-secret-key-123" | Out-File .env

# Load data
python init_db.py

# Start server
python app.py
```

✅ Backend running on `http://localhost:5000`

---

### 2️⃣ Frontend Setup (2 minutes)

**Open NEW PowerShell window:**

```powershell
# Navigate to frontend
cd c:\smart_pg\frontend

# Create .env file
"REACT_APP_API_URL=http://localhost:5000/api" | Out-File .env

# Install dependencies
npm install

# Start development server
npm start
```

✅ Frontend running on `http://localhost:3000`

---

## 🧪 Test the App

1. **Create Account**
   - Click "Register"
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `123456`

2. **Search PGs**
   - Select city: `Kolkata`
   - Budget: Use slider to set ₹20,000
   - Tenant Type: `Bachelors`
   - Click "Get Recommendations"

3. **View Results**
   - You'll see PG cards
   - Click any card for details
   - See similar PGs section

4. **Logout**
   - Click your username
   - Click "Logout"

---

## ⚠️ If Something Goes Wrong

### Backend not starting?
```powershell
# Delete database and reinitialize
Remove-Item database.db
python init_db.py
```

### Port 5000 in use?
```powershell
# Kill process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### NPM install failing?
```powershell
# Clear cache and try again
npm cache clean --force
npm install
```

### CSV not found?
```
Ensure file is at: c:\smart_pg\data\House_Rent_Dataset.csv
```

---

## 📚 What Gets Created

### Database Tables
- `users` - User accounts
- `pgs` - Property listings
- `saved_pgs` - Favorites
- `reviews` - User reviews
- `amenities` - Property features

### Backend Structure
```
backend/
├── app.py (Flask server)
├── models.py (Database models)
├── ml_model.py (Recommendation engine)
├── routes/ (API endpoints)
└── database.db (SQLite database)
```

### Frontend Structure
```
frontend/
├── src/
│   ├── pages/ (Home, Results, Details, Auth)
│   ├── components/ (Layout, Routes)
│   ├── context/ (Auth state)
│   └── api/ (API client)
└── public/index.html
```

---

## 📖 Next Steps

After getting everything running:

1. **Explore the ML Model**
   - Edit `backend/ml_model.py` to customize recommendations
   - Adjust filtering logic
   - Change similarity algorithm

2. **Customize Styling**
   - Modify `frontend/src/index.css`
   - Edit Tailwind config in `frontend/tailwind.config.js`
   - Change colors in `frontend/src/components/Layout.jsx`

3. **Add Features**
   - Save favorite PGs (add to backend)
   - User reviews system
   - Email notifications
   - Advanced filters

4. **Deploy**
   - Backend: Railway, Render, Heroku
   - Frontend: Vercel, Netlify
   - Database: PostgreSQL cloud

---

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| Port 5000 in use | Kill process on that port |
| Virtual env not activating | Check if Python is in PATH |
| npm install slow | Check internet, try `npm cache clean --force` |
| API 401 errors | Ensure backend is running on port 5000 |
| CSV loading fails | Check file path and encoding (UTF-8) |

---

## 📊 Database Verification

After initialization, verify data was loaded:

```powershell
cd c:\smart_pg\backend
python

# In Python shell:
from app import app, db
from models import PG

with app.app_context():
    count = PG.query.count()
    print(f"Total PGs in database: {count}")
    
    cities = db.session.query(PG.city).distinct().all()
    print(f"Cities: {[c[0] for c in cities[:5]]}")
```

---

**That's it! You're ready to go! 🎉**

For detailed documentation, see `README.md`.
