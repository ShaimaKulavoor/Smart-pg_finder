# Smart PG Finder - Complete Setup Guide

This is a full-stack PG (Paying Guest) recommendation web application with:
- **Backend**: Flask + ML recommendation engine
- **Frontend**: React with Tailwind CSS
- **Database**: SQLite with user authentication
- **ML**: Content-based filtering using scikit-learn

## 📋 Prerequisites

Before starting, ensure you have:
- **Python 3.8+** installed
- **Node.js 14+** and npm installed
- **Git** (optional)

### Windows Installation

#### Python
1. Download from https://www.python.org/downloads/
2. During installation, **check "Add Python to PATH"**
3. Verify: Open PowerShell and run:
   ```
   python --version
   ```

#### Node.js
1. Download from https://nodejs.org/ (LTS version)
2. Run the installer and follow prompts
3. Verify: Open PowerShell and run:
   ```
   node --version
   npm --version
   ```

---

## 🚀 STEP-BY-STEP SETUP

### Step 1: Prepare the Project

1. Navigate to the project folder:
   ```
   cd c:\smart_pg
   ```

2. Copy the CSV dataset to the data folder:
   - Place your `House_Rent_Dataset.csv` in `c:\smart_pg\data\`

---

### Step 2: Backend Setup

#### 2.1 Create Python Virtual Environment

```
cd c:\smart_pg\backend
python -m venv venv
```

#### 2.2 Activate Virtual Environment

**On Windows (PowerShell):**
```
.\venv\Scripts\Activate.ps1
```

**If you get an error**, try:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` at the beginning of the terminal line.

#### 2.3 Install Backend Dependencies

```
pip install -r requirements.txt
```

This will install:
- Flask
- SQLAlchemy
- Flask-CORS
- pandas
- scikit-learn
- PyJWT

#### 2.4 Create Environment File

Create a file `c:\smart_pg\backend\.env`:

```
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///database.db
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_EXPIRATION_DELTA=7
CORS_ORIGINS=http://localhost:3000,http://localhost:5000
```

#### 2.5 Load Data into Database

Create a file `c:\smart_pg\backend\init_db.py`:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app
from load_data import load_data_to_db

# Load data
csv_path = '../data/House_Rent_Dataset.csv'
load_data_to_db(csv_path, app)
```

Then run:
```
python init_db.py
```

This will:
- Load CSV data into SQLite database
- Create all tables
- Add 50+ PG listings
- Set up amenities

#### 2.6 Start Backend Server

```
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
* Press CTRL+C to quit
```

✅ Backend is ready!

---

### Step 3: Frontend Setup

#### 3.1 Navigate to Frontend

In a **NEW PowerShell window**:
```
cd c:\smart_pg\frontend
```

#### 3.2 Create Environment File

Create a file `c:\smart_pg\frontend\.env`:

```
REACT_APP_API_URL=http://localhost:5000/api
```

#### 3.3 Install Frontend Dependencies

```
npm install
```

This will install React, React Router, Axios, Tailwind CSS, and more.
(This may take 2-3 minutes)

#### 3.4 Start Frontend Server

```
npm start
```

This will:
- Start the React development server
- Open browser at http://localhost:3000
- Auto-reload on code changes

🎉 **Application is now running!**

---

## 📱 Testing the Application

### 3.1 Create a User Account

1. Go to http://localhost:3000
2. Click "Register" button
3. Fill in:
   - **Username:** testuser
   - **Email:** test@example.com
   - **Password:** password123
4. Click "Register"

### 3.2 Login

1. Now on login page, enter:
   - **Username:** testuser
   - **Password:** password123
2. Click "Login"

### 3.3 Search for PGs

1. On home page, select:
   - **City:** Kolkata (or any from dropdown)
   - **Budget:** Drag slider to 20000
   - **Tenant Type:** Bachelors
2. Click "Get Recommendations"

### 3.4 View Results

You should see:
- 5-10 PG listings matching your criteria
- Click any card to view full details
- See amenities, reviews, ratings
- Similar PGs section

### 3.5 Test Login/Logout

- Click your username in top right
- Click "Logout"
- You should be redirected to login page

---

## 🔧 How the ML Recommendation System Works

The backend uses **Content-Based Collaborative Filtering**:

1. **Feature Extraction**: Combines city, locality, furnishing, and tenant type
2. **TF-IDF Vectorization**: Converts text features to numerical vectors
3. **Cosine Similarity**: Calculates similarity between PGs
4. **Ranking**: Returns top recommendations sorted by price and rating

### Example Flow:
- User enters: Bangalore, Budget 15000, Bachelors
- Backend filters: PGs ≤ ₹15000 for Bachelors in Bangalore
- ML ranks by location similarity and price
- Returns top 5 recommendations

---

## 📊 API Endpoints

### Authentication
```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET /api/auth/verify-token
GET /api/auth/profile
```

### Recommendations
```
GET /api/recommend?city=Bangalore&max_budget=15000&tenant_type=Bachelors
GET /api/pg/<id>                    - Get PG details
GET /api/filter?city=Bangalore      - Advanced filtering
GET /api/cities                     - List all cities
GET /api/localities/<city>          - Localities in a city
GET /api/stats                      - General statistics
```

---

## 🐛 Troubleshooting

### Backend won't start
- Check if port 5000 is in use: Kill the process or change port in `app.py`
- Ensure virtual environment is activated: `.\venv\Scripts\Activate.ps1`
- Check database error: Delete `database.db` and run `init_db.py` again

### Frontend connection error
- Ensure backend is running on `http://localhost:5000`
- Check `.env` file has correct API URL
- Clear browser cache: Ctrl+Shift+Delete → Clear all

### CSV not loading
- Verify file path in `init_db.py`
- File must be named `House_Rent_Dataset.csv`
- Check for encoding issues (UTF-8)

### Port 5000/3000 already in use
```
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F
```

---

## 📁 Project Structure

```
smart_pg/
├── backend/
│   ├── app.py                 (Main Flask app)
│   ├── models.py              (Database models)
│   ├── ml_model.py            (ML recommendation engine)
│   ├── load_data.py           (CSV data loader)
│   ├── routes/
│   │   ├── auth_routes.py     (Authentication APIs)
│   │   └── recommendation_routes.py (Recommendation APIs)
│   ├── requirements.txt        (Python dependencies)
│   └── venv/                  (Virtual environment)
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.jsx            (Main component)
│   │   ├── index.js           (Entry point)
│   │   ├── index.css          (Styles)
│   │   ├── api/
│   │   │   └── api.js         (API client)
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
│   ├── package.json           (npm dependencies)
│   └── node_modules/          (installed packages)
│
├── data/
│   └── House_Rent_Dataset.csv
│
└── README.md (this file)
```

---

## 🔑 Key Features Implemented

✅ **Home Page**
- City selector dropdown
- Budget range slider
- Tenant type selector
- Move-in/Move-out dates
- Guest count selector
- "Get Recommendations" call-to-action

✅ **Results Page**
- Grid of PG cards with images
- Sorting by price, rating, size
- Applied filters display
- Pagination indicator

✅ **Details Page**
- Full PG information
- Amenities list with availability
- Ratings & reviews section
- Similar PG recommendations
- Book Now & Contact Owner buttons

✅ **Authentication**
- User registration with validation
- Login with JWT tokens
- Session persistence
- Logout functionality
- Protected routes (if needed)

✅ **Backend**
- RESTful API design
- Data validation & error handling
- ML-based recommendations
- Database operations
- Proper HTTP status codes

✅ **Frontend**
- Responsive design (mobile, tablet, desktop)
- Tailwind CSS styling
- React Router for navigation
- Axios for API calls
- Loading states
- Error handling

---

## 🚀 Deployment Tips

### Backend Deployment (Production)
1. Set `FLASK_ENV=production`
2. Use strong `SECRET_KEY`
3. Use PostgreSQL instead of SQLite
4. Enable HTTPS/SSL
5. Set secure CORS origins
6. Use environment variables for secrets

### Frontend Deployment
1. Run `npm run build`
2. Deploy `/build` folder to:
   - Vercel
   - Netlify
   - GitHub Pages
   - Your own server

### Example: Deploy to Vercel
```
npm install -g vercel
vercel login
vercel
```

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review API endpoints documentation
3. Check browser console for errors (F12)
4. Check terminal for backend errors

---

## 📄 License

This project is for educational purposes. Feel free to modify and use as needed.

---

**Happy PG Hunting! 🏠✨**
