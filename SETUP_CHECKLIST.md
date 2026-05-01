# 📋 SETUP CHECKLIST & INSTALLATION GUIDE

## ✅ Pre-Installation Checklist

Before starting, verify:

- [ ] Python 3.8+ installed
  ```powershell
  python --version
  ```

- [ ] Node.js 14+ and npm installed
  ```powershell
  node --version
  npm --version
  ```

- [ ] CSV file copied to `data/House_Rent_Dataset.csv`
  ```powershell
  Get-Item c:\smart_pg\data\House_Rent_Dataset.csv
  ```

- [ ] Git installed (optional)
  ```powershell
  git --version
  ```

---

## 🔧 PART 1: BACKEND INSTALLATION

### Step 1.1: Navigate to Backend Directory

```powershell
cd c:\smart_pg\backend
```

### Step 1.2: Create Python Virtual Environment

```powershell
python -m venv venv
```

**What this does:**
- Creates isolated Python environment
- Keeps project dependencies separate
- Prevents conflicts with other Python projects

### Step 1.3: Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

**Expected output:**
```
(venv) PS C:\smart_pg\backend>
```

**If it fails with execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### Step 1.4: Upgrade pip (Optional but Recommended)

```powershell
python -m pip install --upgrade pip
```

### Step 1.5: Install Python Dependencies

```powershell
pip install -r requirements.txt
```

**What gets installed:**
- Flask (web framework)
- SQLAlchemy (database ORM)
- Flask-CORS (cross-origin requests)
- pandas (data manipulation)
- scikit-learn (machine learning)
- PyJWT (authentication tokens)
- Werkzeug (security utilities)

**Wait time:** 2-3 minutes

### Step 1.6: Create Environment File

Create file: `c:\smart_pg\backend\.env`

**On PowerShell:**
```powershell
@"
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///database.db
SECRET_KEY=your-super-secret-key-change-this-in-production-12345
JWT_EXPIRATION_DELTA=7
CORS_ORIGINS=http://localhost:3000
"@ | Out-File .env -Encoding UTF8
```

**Or create manually with notepad:**
```
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///database.db
SECRET_KEY=your-super-secret-key-change-in-production
JWT_EXPIRATION_DELTA=7
CORS_ORIGINS=http://localhost:3000
```

### Step 1.7: Initialize Database

```powershell
python init_db.py
```

**What happens:**
- Reads CSV file from `../data/House_Rent_Dataset.csv`
- Creates `database.db` SQLite database
- Creates tables: users, pgs, amenities, reviews, saved_pgs
- Loads all PG listings
- Adds default amenities

**Expected output:**
```
============================================================
  SMART PG FINDER - DATABASE INITIALIZATION
============================================================

📁 Loading data from CSV...
✓ Loaded 10500 records from CSV
...
✓ Successfully loaded 5000+ PGs into database!
✓ Database initialization complete!
```

### Step 1.8: Start Backend Server

```powershell
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

✅ **Backend is running!** Keep this terminal open.

---

## 🎨 PART 2: FRONTEND INSTALLATION

### Step 2.1: Open New PowerShell Window

**Do NOT close the backend terminal!**

Open a new PowerShell window (or tab in Windows Terminal)

### Step 2.2: Navigate to Frontend

```powershell
cd c:\smart_pg\frontend
```

### Step 2.3: Create Environment File

Create file: `c:\smart_pg\frontend\.env`

```powershell
@"
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
"@ | Out-File .env -Encoding UTF8
```

### Step 2.4: Install Node Dependencies

```powershell
npm install
```

**What gets installed:**
- React 18 (UI library)
- React Router (navigation)
- Axios (HTTP client)
- Tailwind CSS (styling)
- 100+ other packages

**Wait time:** 2-5 minutes (depends on internet speed)

**If it hangs, try:**
```powershell
npm cache clean --force
npm install
```

### Step 2.5: Start Frontend Development Server

```powershell
npm start
```

**Expected output:**
```
Compiled successfully!

You can now view smart-pg-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://xxx.xxx.xxx.xxx:3000

Note that the development build is not optimized.
```

**Browser should open automatically to http://localhost:3000**

✅ **Frontend is running!**

---

## 🧪 PART 3: APPLICATION TESTING

### Step 3.1: Register a Test User

1. On http://localhost:3000, click **"Register"**
2. Fill in:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `password123`
3. Click **"Register"**

### Step 3.2: Login

1. After registration, click **"Login"**
2. Enter:
   - Username: `testuser`
   - Password: `password123`
3. Click **"Login"**

### Step 3.3: Test Home Page

You should see:
- ✅ City dropdown (shows cities from CSV)
- ✅ Budget slider (5K to 100K)
- ✅ Tenant type selector
- ✅ Date pickers
- ✅ Guest counter
- ✅ "Get Recommendations" button

### Step 3.4: Search for PGs

1. **Select city:** `Kolkata` (or any from dropdown)
2. **Set budget:** Drag slider to `₹20,000`
3. **Select tenant:** `Bachelors/Family`
4. Click **"Get Recommendations"**

### Step 3.5: View Results

You should see:
- ✅ List of 5-10 PG cards
- ✅ Each card shows: image, rent, rating, BHK, size
- ✅ Sort options (by price, rating, size)
- ✅ Applied filters display

### Step 3.6: View PG Details

1. Click on any PG card
2. You should see:
   - ✅ Full property details
   - ✅ Amenities list
   - ✅ Ratings & reviews
   - ✅ Similar recommendations
   - ✅ "Book Now" and "Contact Owner" buttons

### Step 3.7: Test Navigation

- ✅ Click back button
- ✅ Navigate between pages
- ✅ Use browser back/forward buttons

### Step 3.8: Test Logout

1. Click your username in top right
2. Click **"Logout"**
3. You should be redirected to login page

---

## 🔍 VERIFICATION CHECKS

### Backend Verification

Open PowerShell and check database:

```powershell
cd c:\smart_pg\backend
# Make sure venv is activated
python

# Inside Python:
from app import app, db
from models import PG

with app.app_context():
    count = PG.query.count()
    print(f"Total PGs: {count}")
    
    city_count = db.session.query(PG.city).distinct().count()
    print(f"Total cities: {city_count}")
    
    cities = db.session.query(PG.city).distinct().limit(5).all()
    print(f"Sample cities: {[c[0] for c in cities]}")

# Type: exit()
```

**Expected output:**
```
Total PGs: 1000+
Total cities: 5+
Sample cities: ['Kolkata', 'Bangalore', ...]
```

### Frontend Verification

1. Check browser console (F12 → Console)
   - Should NOT show major errors
   - May show warnings (safe to ignore)

2. Check network tab (F12 → Network)
   - API calls to `http://localhost:5000/api/...` should work
   - Status 200, 201 = success

3. Test localStorage
   - Open F12 → Application → Local Storage
   - Should see `authToken` and `currentUser` after login

---

## ⚠️ TROUBLESHOOTING

### Issue: Backend won't start

**Error message might show:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```powershell
# Find process on port 5000
netstat -ano | findstr :5000

# Kill the process (replace 1234 with actual PID)
taskkill /PID 1234 /F
```

---

### Issue: Virtual environment won't activate

**Error:**
```
cannot be loaded because running scripts is disabled on this system
```

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Type: Y (Yes)
.\venv\Scripts\Activate.ps1
```

---

### Issue: npm install is slow or failing

**Solution:**
```powershell
# Clear npm cache
npm cache clean --force

# Try again
npm install

# If still slow, try:
npm install --legacy-peer-deps
```

---

### Issue: CSV file not loading to database

**Check 1: File exists**
```powershell
Get-Item c:\smart_pg\data\House_Rent_Dataset.csv
```

**Check 2: File format**
- Must be CSV format
- Must be UTF-8 encoded
- Column names should match expected columns

**Check 3: Try loading manually**
```powershell
cd c:\smart_pg\backend
python init_db.py
# Follow prompts and specify path: ../data/House_Rent_Dataset.csv
```

---

### Issue: API connection errors in frontend

**Error in browser console:**
```
GET http://localhost:5000/api/cities 404
```

**Solution:**
1. Verify backend is running (should see terminal with Flask running)
2. Check `.env` file has correct API URL: `REACT_APP_API_URL=http://localhost:5000/api`
3. Restart frontend: `npm start`

---

### Issue: Login not working

**Steps to debug:**
1. Check backend console for errors
2. Verify user exists in database:
   ```powershell
   python
   from app import app, db
   from models import User
   
   with app.app_context():
       user = User.query.filter_by(username='testuser').first()
       print(user)
   ```
3. Check browser console for errors
4. Verify token is being saved in localStorage

---

## 🚀 RUNNING THE APPLICATION (Daily Use)

### To Start Application:

**Terminal 1: Backend**
```powershell
cd c:\smart_pg\backend
.\venv\Scripts\Activate.ps1
python app.py
```

**Terminal 2: Frontend**
```powershell
cd c:\smart_pg\frontend
npm start
```

### To Stop Application:

- **Backend:** Press `CTRL + C` in backend terminal
- **Frontend:** Press `CTRL + C` in frontend terminal

---

## 📁 Verified Directory Structure

After successful setup, you should have:

```
c:\smart_pg\
├── README.md                 ← Detailed documentation
├── QUICK_START.md           ← Quick start guide
├── API_DOCS.md              ← API reference
├── SETUP_CHECKLIST.md       ← This file
│
├── backend/
│   ├── venv/                ← Virtual environment (created by you)
│   ├── database.db          ← SQLite database (created by init_db.py)
│   ├── app.py               ← Main Flask app
│   ├── models.py            ← Database models
│   ├── ml_model.py          ← ML recommendation engine
│   ├── load_data.py         ← Data loading script
│   ├── init_db.py           ← Database initialization
│   ├── requirements.txt      ← Python dependencies
│   ├── .env                 ← Environment variables (created by you)
│   └── routes/
│       ├── auth_routes.py
│       └── recommendation_routes.py
│
├── frontend/
│   ├── node_modules/        ← NPM packages (created by npm install)
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.js
│   │   ├── index.css
│   │   ├── api/
│   │   │   └── api.js
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── ResultsPage.jsx
│   │   │   ├── DetailsPage.jsx
│   │   │   └── AuthPages.jsx
│   │   ├── components/
│   │   │   ├── Layout.jsx
│   │   │   └── PrivateRoute.jsx
│   │   └── context/
│   │       └── AuthContext.jsx
│   ├── package.json
│   ├── .env                 ← Environment variables (created by you)
│   └── tailwind.config.js
│
└── data/
    └── House_Rent_Dataset.csv
```

---

## ✨ Success Indicators

You'll know everything is working when:

✅ Backend terminal shows: `Running on http://127.0.0.1:5000`
✅ Frontend opens automatically in browser at `http://localhost:3000`
✅ No major errors in browser console
✅ Can register and login successfully
✅ Can search for PGs and see results
✅ Can click on results and see full details
✅ Database has 1000+ PG listings

---

## 📞 Quick Help

| Problem | Command |
|---------|---------|
| Activate venv | `.\venv\Scripts\Activate.ps1` |
| Check Python | `python --version` |
| Check Node | `node --version` |
| Clear npm cache | `npm cache clean --force` |
| Delete database | `Remove-Item database.db` |
| Kill port 5000 | `netstat -ano \| findstr :5000` |

---

## 🎓 Learning Resources

**Backend (Flask):**
- Flask docs: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- JWT auth: https://pyjwt.readthedocs.io/

**Frontend (React):**
- React docs: https://react.dev/
- React Router: https://reactrouter.com/
- Tailwind CSS: https://tailwindcss.com/

**Machine Learning:**
- scikit-learn: https://scikit-learn.org/
- Pandas: https://pandas.pydata.org/

---

## 🎉 You're Done!

Congratulations! Your Smart PG Finder application is ready.

### Next Steps:
1. Explore the application
2. Test all features
3. Check API endpoints in API_DOCS.md
4. Customize styles or add features
5. Deploy when ready!

---

**Happy coding! 🚀**
