# 🚀 SMART PG FINDER - COMPLETE RUN GUIDE

## ✅ Pre-Requisites

Before starting, ensure you have:
- **Python 3.8+** installed
- **Node.js 14+** and npm installed
- **Git** (optional)

### Verify Installation

Open PowerShell and run:
```powershell
python --version
node --version
npm --version
```

---

## 📁 PROJECT STRUCTURE

```
c:\smart_pg\
├── backend/                    # Flask API
│   ├── app.py                 # Main app
│   ├── models.py              # Database models
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── recommendation_routes.py
│   │   └── chat_routes.py
│   ├── ml_model.py            # ML recommendation engine
│   ├── load_data.py           # Data loader
│   ├── requirements.txt       # Python dependencies
│   └── instance/              # Database (created after first run)
│
├── frontend/                   # React App
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── api/
│   ├── package.json           # npm dependencies
│   └── public/
│
├── data/
│   └── House_Rent_Dataset.csv # Dataset (must be placed here)
│
└── notebooks/
    └── pg_rec.ipynb           # Jupyter notebook (reference)
```

---

## 🔧 STEP 1: BACKEND SETUP

### 1.1 Create Python Virtual Environment

Navigate to project folder:
```powershell
cd c:\smart_pg
python -m venv .venv
```

### 1.2 Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If you get execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 1.3 Install Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

### 1.4 Prepare Dataset

1. Make sure `House_Rent_Dataset.csv` is in `c:\smart_pg\data\`
2. Check that the CSV file has these columns:
   - `posted_on`
   - `bhk`
   - `rent`
   - `size`
   - `floor`
   - `area_type`
   - `area_locality`
   - `city`
   - `furnishing_status`
   - `tenant_preferred`
   - `bathroom`
   - `point_of_contact`

### 1.5 Initialize Database & Load Data

```powershell
cd c:\smart_pg\backend
python init_db.py
```

When prompted, enter the CSV path or press Enter for default:
```
Enter path to CSV file (default: ../data/House_Rent_Dataset.csv): 
```

Wait for the process to complete. You should see:
```
✓ Successfully loaded XXXX PGs into database!
✓ Database initialization complete!
```

### 1.6 Start Backend Server

```powershell
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000/
```

**Keep this terminal running!** Open a new PowerShell tab for frontend setup.

---

## 🎨 STEP 2: FRONTEND SETUP

### 2.1 Navigate to Frontend Directory

In a **new PowerShell tab**:
```powershell
cd c:\smart_pg\frontend
```

### 2.2 Install Dependencies

```powershell
npm install
```

This will download all required packages. Wait for it to complete.

### 2.3 Start React Development Server

```powershell
npm start
```

Wait for it to compile. You should see:
```
Compiled successfully!
Local: http://localhost:3000
```

Your browser should automatically open at `http://localhost:3000`. If not, open it manually.

---

## ✅ VERIFY SETUP

### Backend Health Check

Open browser and visit:
```
http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "ok",
  "message": "Smart PG Recommendation API is running"
}
```

### Frontend Status

App should open at `http://localhost:3000` with:
- Header with Smart PG logo
- Search form with city dropdown
- Hero section

---

## 🧪 TESTING GUIDE

### Test 1: Register New User

1. Click **"Register"** button in header
2. Fill in:
   - Username: `testuser1`
   - Email: `test@example.com`
   - Password: `password123`
   - Confirm Password: `password123`
3. Click **"Register"**
4. Should redirect to login page with success message

### Test 2: Login

1. Click **"Login"**
2. Enter:
   - Username: `testuser1`
   - Password: `password123`
3. Click **"Login"**
4. Should redirect to home page

### Test 3: Get Recommendations

1. From home page, select:
   - City: `Bangalore` (or any available city)
   - Budget: Adjust slider (default: ₹15,000)
   - Tenant Type: `Bachelors` or `Family`
2. Click **"🔍 Get Recommendations"**
3. Should show search results with PG cards in grid layout

### Test 4: View PG Details

1. From results, click any PG card
2. Should show detailed information:
   - Images
   - Full description
   - Amenities
   - Similar PGs
   - Reviews

### Test 5: Save as Favorite (When Logged In)

1. From PG details page, click heart icon (❤️)
2. Should show confirmation message
3. Visit profile to see saved favorites

### Test 6: Use Chatbot

1. Look for 💬 button at bottom-right of screen
2. Click to open chatbot
3. Try messages like:
   - "Show me PGs under 10000"
   - "Find 2BHK in Bangalore"
   - "Bachelors friendly"
4. Should return filtered recommendations

### Test 7: Filter Recommendations

1. On results page, use sort dropdown:
   - Sort by Price
   - Sort by Rating
   - Sort by Size
2. Results should reorder accordingly

---

## 🐛 TROUBLESHOOTING

### Issue: "Cannot find module"

**Solution:**
```powershell
cd backend
pip install -r requirements.txt
```

### Issue: Database error "database.db not found"

**Solution:**
```powershell
cd backend
python init_db.py
```

### Issue: Port 5000 or 3000 already in use

**Solution:**
```powershell
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in app.py (line: app.run(..., port=5001))
```

### Issue: Cities dropdown showing "No cities"

**Solution:**
1. Check if CSV file is in correct location: `c:\smart_pg\data\`
2. Run database initialization again:
   ```powershell
   python init_db.py
   ```
3. Check if CSV has 'city' column (case-sensitive in code)

### Issue: Chatbot not responding

**Solution:**
1. Check backend is running (`http://localhost:5000/api/health`)
2. Open browser console (F12) to see error messages
3. Ensure `/api/chat/message` endpoint exists

### Issue: Login fails "Invalid token format"

**Solution:**
1. Restart backend server:
   ```powershell
   # Stop current backend (Ctrl+C)
   python app.py  # Restart
   ```
2. Clear browser cookies and local storage
3. Register new account and try again

---

## 📝 API ENDPOINTS REFERENCE

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/verify-token` - Verify JWT token
- `POST /api/auth/logout` - Logout

### Recommendations
- `GET /api/recommend` - Get recommendations
- `GET /api/pg/<id>` - Get PG details
- `GET /api/filter` - Filter PGs
- `GET /api/cities` - Get available cities
- `GET /api/localities/<city>` - Get localities in city

### Favorites (Requires Auth)
- `GET /api/favorites` - Get saved PGs
- `POST /api/favorites/<pg_id>` - Save PG
- `DELETE /api/favorites/<pg_id>` - Remove from favorites

### Chatbot
- `POST /api/chat/message` - Send message to chatbot
- `GET /api/chat/suggestions` - Get chat suggestions

---

## 🔐 ENVIRONMENT VARIABLES

Create `.env` file in backend folder:

```
# backend/.env
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
```

Or edit values in `app.py`:
```python
app.config['SECRET_KEY'] = 'your-secure-key'
```

---

## 📦 DEPLOYMENT CHECKLIST

- [ ] Database initialized with CSV data
- [ ] Backend starts without errors
- [ ] Frontend loads without errors
- [ ] Can register and login
- [ ] Can get recommendations
- [ ] Chatbot responds
- [ ] Favorites system works
- [ ] All pages responsive (test on mobile)

---

## 🎯 NEXT STEPS

1. **Customize dataset**: Replace CSV with your own PG data
2. **Add images**: Update image URLs in database
3. **Configure Groq API**: For advanced chatbot features
4. **Deploy to cloud**: Use Heroku, AWS, or Azure
5. **Add more features**: Reviews, ratings, messaging

---

## 📞 SUPPORT

For issues, check:
1. Backend logs in terminal
2. Browser console (F12 → Console tab)
3. Network tab to see API calls
4. Database file exists: `backend/instance/database.db`

---

## ✨ FEATURES IMPLEMENTED

✅ User Registration & Login (JWT)
✅ City Dynamic Dropdown
✅ AI Recommendations (ML Model)
✅ Advanced Filtering
✅ PG Details Page
✅ Save Favorites
✅ Chatbot with Intent Recognition
✅ Responsive Design
✅ Modern UI with Tailwind CSS
✅ Smooth Animations
✅ Error Handling
✅ Loading States

---

**Good luck! 🚀 Enjoy building your Smart PG Finder!**
