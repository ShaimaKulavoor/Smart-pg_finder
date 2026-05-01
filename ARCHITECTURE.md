# 🏗️ SYSTEM ARCHITECTURE & DATA FLOW

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        SMART PG FINDER                          │
│                     FULL-STACK APPLICATION                       │
└─────────────────────────────────────────────────────────────────┘

                                
┌──────────────────────────┐          ┌──────────────────────────┐
│                          │          │                          │
│   FRONTEND (React)       │          │   BACKEND (Flask)        │
│   Port: 3000             │          │   Port: 5000             │
│                          │          │                          │
├──────────────────────────┤          ├──────────────────────────┤
│                          │          │                          │
│ ┌────────────────────┐   │          │ ┌────────────────────┐   │
│ │   Pages            │   │          │ │ Routes             │   │
│ ├────────────────────┤   │          │ ├────────────────────┤   │
│ │ • HomePage         │   │<──HTTP───│ │ • auth_routes.py   │   │
│ │ • ResultsPage      │──────Axios──→├────────────────────┤   │ 
│ │ • DetailsPage      │   │  (JSON)  │ │ • recommend_       │   │
│ │ • AuthPages        │   │          │ │   routes.py        │   │
│ └────────────────────┘   │          │ └────────────────────┘   │
│                          │          │                          │
│ ┌────────────────────┐   │          │ ┌────────────────────┐   │
│ │   Components       │   │          │ │ Controllers        │   │
│ ├────────────────────┤   │          │ ├────────────────────┤   │
│ │ • Layout.jsx       │   │          │ │ • app.py           │   │
│ │ • PrivateRoute.jsx │   │          │ │ • ml_model.py      │   │
│ └────────────────────┘   │          │ └────────────────────┘   │
│                          │          │                          │
│ ┌────────────────────┐   │          │ ┌────────────────────┐   │
│ │   Utils            │   │          │ │ Models & DB        │   │
│ ├────────────────────┤   │  REST    │ ├────────────────────┤   │
│ │ • api.js (Axios)   │───────API────→│ • models.py        │   │
│ │ • AuthContext.jsx  │   │          │ • database.db      │   │
│ └────────────────────┘   │          │ └────────────────────┘   │
│                          │          │                          │
│ ┌────────────────────┐   │          │ ┌────────────────────┐   │
│ │   Styling          │   │          │ │ ML Engine          │   │
│ ├────────────────────┤   │          │ ├────────────────────┤   │
│ │ • Tailwind CSS     │   │          │ │ • Recommendations  │   │
│ │ • index.css        │   │          │ │ • Feature Extraction
│ └────────────────────┘   │          │ │ • Similarity       │   │
│                          │          │ └────────────────────┘   │
└──────────────────────────┘          └──────────────────────────┘

                  │
                  │ Database Connection
                  ↓
        
┌──────────────────────────────────────┐
│      SQLite DATABASE                 │
│      database.db                     │
├──────────────────────────────────────┤
│                                      │
│  ┌──────────────────────────────┐   │
│  │ users table                  │   │
│  ├──────────────────────────────┤   │
│  │ • id (PK)                    │   │
│  │ • username                   │   │
│  │ • email                      │   │
│  │ • password_hash              │   │
│  └──────────────────────────────┘   │
│                                      │
│  ┌──────────────────────────────┐   │
│  │ pgs table                    │   │
│  ├──────────────────────────────┤   │
│  │ • id (PK)                    │   │
│  │ • bhk, rent, size            │   │
│  │ • city, locality             │   │
│  │ • furnishing_status          │   │
│  │ • tenant_preferred           │   │
│  │ • rating, image_url          │   │
│  └──────────────────────────────┘   │
│                                      │
│  ┌──────────────────────────────┐   │
│  │ amenities table              │   │
│  ├──────────────────────────────┤   │
│  │ • id (PK)                    │   │
│  │ • pg_id (FK)                 │   │
│  │ • name, available            │   │
│  └──────────────────────────────┘   │
│                                      │
│  ┌──────────────────────────────┐   │
│  │ reviews table                │   │
│  ├──────────────────────────────┤   │
│  │ • id (PK)                    │   │
│  │ • user_id (FK)               │   │
│  │ • pg_id (FK)                 │   │
│  │ • rating, comment            │   │
│  └──────────────────────────────┘   │
│                                      │
│  ┌──────────────────────────────┐   │
│  │ saved_pgs table              │   │
│  ├──────────────────────────────┤   │
│  │ • id (PK)                    │   │
│  │ • user_id (FK)               │   │
│  │ • pg_id (FK)                 │   │
│  └──────────────────────────────┘   │
│                                      │
└──────────────────────────────────────┘
```

---

## Request/Response Flow

### 1. User Registration Flow

```
User (Frontend)
    │
    ├─→ [Enter credentials]
    │
    └─→ POST /api/auth/register (JSON)
        {
          "username": "testuser",
          "email": "test@example.com",
          "password": "password123"
        }
        
        ↓
        
    Flask Backend
        │
        ├─→ Validations
        │   • Check username not taken
        │   • Check email not taken
        │   • Validate password strength
        │
        ├─→ Hash Password
        │   • werkzeug.security.generate_password_hash
        │
        ├─→ Create User Record
        │   • INSERT INTO users table
        │
        └─→ Return:
            {
              "status": "success",
              "user": { id, username, email }
            }
        
        ↓
        
    Frontend
        │
        ├─→ Store response
        ├─→ Redirect to login
        └─→ Show success message
```

### 2. User Login Flow

```
User (Frontend)
    │
    ├─→ [Enter credentials]
    │
    └─→ POST /api/auth/login (JSON)
        {
          "username": "testuser",
          "password": "password123"
        }
        
        ↓
        
    Flask Backend
        │
        ├─→ Find user by username
        │   • Query users table
        │
        ├─→ Verify password
        │   • check_password_hash(stored_hash, provided_password)
        │
        ├─→ Generate JWT Token
        │   • jwt.encode(payload, secret_key)
        │   • Payload: user_id, username, exp (7 days)
        │
        └─→ Return:
            {
              "status": "success",
              "token": "eyJhbGciOiJIUzI1NiIs...",
              "user": { id, username, email }
            }
        
        ↓
        
    Frontend
        │
        ├─→ Save token to localStorage
        ├─→ Save user to localStorage
        ├─→ Update AuthContext
        ├─→ Redirect to home
        └─→ Include token in all future requests
            Authorization: Bearer <token>
```

### 3. Recommendation Search Flow

```
User (Frontend)
    │
    ├─→ [Fill search form]
    │   • City: Kolkata
    │   • Budget: ₹20,000
    │   • Tenant Type: Bachelors
    │
    └─→ GET /api/recommend?city=Kolkata&max_budget=20000&tenant_type=Bachelors
        
        ↓
        
    Flask Backend
        │
        ├─→ Receive query parameters
        │
        ├─→ Call ML Model (ml_model.py)
        │   • Filter: city == 'Kolkata' AND rent <= 20000 AND tenant_type contains 'Bachelors'
        │
        ├─→ Feature Extraction
        │   • Combine: city + locality + furnishing + tenant_type
        │
        ├─→ Vectorization (TF-IDF)
        │   • Convert text tags to numerical vectors
        │
        ├─→ Calculate Similarity
        │   • cosine_similarity(feature_matrix)
        │
        ├─→ Rank Results
        │   • Sort by: rent (ascending), rating (descending)
        │
        ├─→ Query Database
        │   • SELECT * FROM pgs WHERE conditions
        │   • LIMIT 10
        │
        └─→ Return:
            {
              "status": "success",
              "count": 10,
              "recommendations": [
                {
                  "id": 1,
                  "locality": "...",
                  "rent": 15000,
                  "rating": 4.5,
                  ...
                },
                ...
              ]
            }
        
        ↓
        
    Frontend
        │
        ├─→ Receive recommendations
        ├─→ Display as cards
        ├─→ Load ResultsPage component
        └─→ Allow sorting and filtering
```

### 4. View PG Details Flow

```
User (Frontend)
    │
    ├─→ [Click on PG card]
    │
    └─→ GET /api/pg/1
        
        ↓
        
    Flask Backend
        │
        ├─→ Query PG details
        │   • SELECT * FROM pgs WHERE id = 1
        │
        ├─→ Get amenities
        │   • SELECT * FROM amenities WHERE pg_id = 1
        │
        ├─→ Get reviews
        │   • SELECT * FROM reviews WHERE pg_id = 1
        │   • Include user information
        │
        ├─→ Get similar PGs
        │   • Call ML model similarity function
        │   • Find similar locality properties
        │
        └─→ Return:
            {
              "status": "success",
              "pg": {
                "id": 1,
                "bhk": 2,
                "rent": 15000,
                "amenities": [
                  { "name": "WiFi", "available": true },
                  ...
                ],
                "reviews": [
                  { "user": "...", "rating": 5.0, "comment": "..." },
                  ...
                ],
                "similar_pgs": [...]
              }
            }
        
        ↓
        
    Frontend
        │
        ├─→ Display PG details
        ├─→ Show amenities list
        ├─→ Display reviews
        ├─→ Show similar recommendations
        └─→ Provide booking options
```

---

## Authentication Flow (Token-Based)

```
                    Login
                      │
                      ↓
        ┌─────────────────────────────┐
        │  Generate JWT Token          │
        │  (valid for 7 days)          │
        └─────────────────────────────┘
                      │
                      ↓ Save to localStorage
        ┌─────────────────────────────┐
        │  Client Stores:              │
        │  • authToken                 │
        │  • currentUser (JSON)        │
        └─────────────────────────────┘
                      │
                      ↓ Each API Request
        ┌─────────────────────────────┐
        │  Axios Interceptor:          │
        │  Adds Authorization Header   │
        │  Authorization: Bearer <token>
        └─────────────────────────────┘
                      │
                      ↓
        ┌─────────────────────────────┐
        │  Backend Middleware:         │
        │  • Decode JWT                │
        │  • Verify signature          │
        │  • Check expiration          │
        │  • Validate user             │
        └─────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
    Token Valid            Token Invalid
          │                       │
      Continue               Logout
      Request                Redirect
                            to Login
```

---

## ML Recommendation Algorithm

```
User Input: {city, budget, tenant_type}
        │
        ↓
┌─────────────────────────────────────┐
│ STEP 1: FILTER                      │
│ Query database with WHERE clause    │
└─────────────────────────────────────┘
        │
        ├─ city = "Kolkata"
        ├─ rent <= 20000
        └─ tenant_preferred contains "Bachelors"
        
        ↓
┌─────────────────────────────────────┐
│ STEP 2: FEATURE EXTRACTION          │
│ Combine attributes into text        │
└─────────────────────────────────────┘
        │
        ├─ Property 1: "Kolkata Whitefield Furnished Bachelors"
        ├─ Property 2: "Kolkata Koramangala Semi-Furnished Family"
        └─ ...
        
        ↓
┌─────────────────────────────────────┐
│ STEP 3: VECTORIZATION (TF-IDF)      │
│ Convert text to vectors             │
└─────────────────────────────────────┘
        │
        ├─ Vector 1: [0.5, 0.2, 0.8, 0.3, ...]
        ├─ Vector 2: [0.5, 0.1, 0.3, 0.7, ...]
        └─ ...
        
        ↓
┌─────────────────────────────────────┐
│ STEP 4: SIMILARITY (Cosine)         │
│ Calculate property similarity       │
└─────────────────────────────────────┘
        │
        ├─ Property 1 vs 2: 0.85 similarity
        ├─ Property 1 vs 3: 0.72 similarity
        └─ ...
        
        ↓
┌─────────────────────────────────────┐
│ STEP 5: RANKING                     │
│ Sort by rent, rating, similarity    │
└─────────────────────────────────────┘
        │
        ├─ Rank 1: Best rent + highest rating
        ├─ Rank 2: Next best
        └─ ...
        
        ↓
┌─────────────────────────────────────┐
│ STEP 6: RETURN TOP N                │
│ Return top 5-10 results             │
└─────────────────────────────────────┘
        │
        ↓
    Results: [PG1, PG2, PG3, ...]
```

---

## Component Hierarchy (Frontend)

```
App.jsx (Root)
│
├─ AuthProvider (Context)
│  │
│  └─ BrowserRouter
│     │
│     ├─ Header
│     │  ├─ Logo
│     │  └─ Navigation (Login/Logout)
│     │
│     ├─ Routes
│     │  │
│     │  ├─ / (HomePage)
│     │  │  ├─ HeroSection
│     │  │  ├─ SearchForm
│     │  │  │  ├─ CitySelector
│     │  │  │  ├─ BudgetSlider
│     │  │  │  ├─ TenantTypeSelector
│     │  │  │  ├─ DatePickers
│     │  │  │  └─ GuestCounter
│     │  │  └─ FeaturesSection
│     │  │
│     │  ├─ /results (ResultsPage)
│     │  │  ├─ SearchHeader
│     │  │  ├─ SortOptions
│     │  │  └─ PGCardGrid (Map)
│     │  │     └─ PGCard (Multiple)
│     │  │
│     │  ├─ /pg/:id (DetailsPage)
│     │  │  ├─ BackButton
│     │  │  ├─ HeroImage
│     │  │  ├─ PriceSection
│     │  │  ├─ PropertyDetails
│     │  │  ├─ AmenitiesSection
│     │  │  ├─ ReviewsSection
│     │  │  ├─ BookingButtons
│     │  │  └─ SimilarPGs
│     │  │
│     │  ├─ /login (LoginPage)
│     │  │  ├─ LoginForm
│     │  │  └─ RegisterLink
│     │  │
│     │  └─ /register (RegisterPage)
│     │     ├─ RegisterForm
│     │     └─ LoginLink
│     │
│     ├─ Footer
│     │
│     └─ PrivateRoute (For protected pages)
│
└─ AuthContext
   ├─ user
   ├─ isAuthenticated
   ├─ login()
   └─ logout()
```

---

## Data Flow Summary

```
CSV File (Input)
    ↓
load_data.py (Data Loader)
    ↓
Parse & Clean Data
    ↓
Insert into SQLite Database
    ↓
│
├─→ Frontend (React)
│       ├─ User fills search form
│       ├─ Calls API via Axios
│       └─ Displays results
│
├─→ Backend (Flask)
│       ├─ Receives request
│       ├─ Validates token
│       ├─ Calls ML model
│       ├─ Queries database
│       └─ Returns JSON response
│
└─→ ML Model (scikit-learn)
        ├─ Feature extraction
        ├─ Vectorization
        ├─ Similarity calculation
        └─ Ranking & filtering
```

---

## File I/O Operations

```
Project Folder: c:\smart_pg\
│
├─ backend/
│  ├─ app.py
│  ├─ models.py
│  ├─ database.db ← SQLite database (created/maintained)
│  ├─ venv/ ← Python packages (created by py -m venv)
│  └─ requirements.txt
│
├─ frontend/
│  ├─ node_modules/ ← NPM packages (created by npm install)
│  ├─ src/
│  ├─ public/
│  └─ package.json
│
└─ data/
   └─ House_Rent_Dataset.csv ← Input data
```

---

## Deployment Architecture (Future)

```
┌────────────────────────────────────────────────────────┐
│                    INTERNET                            │
└────────────────────────────────────────────────────────┘
         │                                 │
         ↓                                 ↓
    ┌──────────┐                    ┌──────────────┐
    │ Vercel/  │                    │ Railway/     │
    │ Netlify  │                    │ Render/      │
    │ (React)  │                    │ Heroku       │
    │          │                    │ (Flask)      │
    └──────────┘                    └──────────────┘
         │                                 │
         └─────────────────┬───────────────┘
                           ↓
                    ┌─────────────┐
                    │  PostgreSQL │
                    │ or MongoDB  │
                    │ (Database)  │
                    └─────────────┘
```

---

## Summary

This architecture provides:
- ✅ Separation of concerns (Frontend/Backend)
- ✅ RESTful API design
- ✅ Database normalization
- ✅ JWT authentication
- ✅ ML-based recommendations
- ✅ Responsive UI
- ✅ Scalable structure

All components work together to create a seamless PG recommendation experience!
