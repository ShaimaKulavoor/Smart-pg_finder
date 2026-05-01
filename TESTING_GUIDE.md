# 🧪 SMART PG FINDER - COMPLETE TESTING GUIDE

## Overview
This guide walks through testing all new features added in the latest upgrade:
- ✅ Image Support
- ✅ Global Chatbot
- ✅ Groq API Integration
- ✅ UI Animations & Skeleton Loaders

---

## 📸 PART 1: IMAGE SUPPORT TESTING

### 1.1 Image Placement
**Location**: Images should be at:
```
c:\smart_pg\frontend\public\images\pg\pg_placeholder_1.svg (through pg_placeholder_5.svg)
```

**Verify**:
```powershell
dir c:\smart_pg\frontend\public\images\pg\
```

Expected output: 5 SVG files (`pg_placeholder_1.svg` through `pg_placeholder_5.svg`)

### 1.2 Database Image URLs
**What Happens**:
- When database loads, each PG gets a random image from the 5 placeholders
- Image URL format: `/images/pg/pg_placeholder_X.svg`

**To Verify**:
```bash
# Start backend
cd c:\smart_pg\backend
c:\smart_pg\venv\Scripts\python.exe app.py

# In another terminal, test API:
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/recommend?city=Kolkata&max_budget=15000" -UseBasicParsing
$data = $response.Content | ConvertFrom-Json
$data.recommendations[0] | Select-Object area_locality, image_url
```

Expected: Each PG has an `image_url` like `/images/pg/pg_placeholder_2.svg`

### 1.3 Frontend Image Display
**Steps**:
1. Start frontend: `npm start` (in `c:\smart_pg\frontend`)
2. Go to http://localhost:3000
3. Select a city and click "Get Recommendations"
4. **Check**: Each PG card shows an image with gradient overlay on hover

**Expected Behavior**:
- ✅ Images load correctly in cards
- ✅ Fallback image appears if image fails (onError handler)
- ✅ Image zooms on hover (3D effect)
- ✅ "View Details" text appears on hover

### 1.4 Image Upload API (Optional)
**Test File Upload**:
```bash
# Create test image
$testFile = "c:\smart_pg\test_image.svg"

# Upload using PowerShell
$filePath = $testFile
$url = "http://localhost:5000/api/upload-image"
$fileBytes = [System.IO.File]::ReadAllBytes($filePath)
$boundary = [System.Guid]::NewGuid().ToString()

$bodyLines = @(
    "--$boundary",
    'Content-Disposition: form-data; name="file"; filename="test.svg"',
    "Content-Type: image/svg+xml",
    "",
    [System.Text.Encoding]::UTF8.GetString($fileBytes),
    "--$boundary--"
)
$body = [System.Text.Encoding]::UTF8.GetBytes(($bodyLines -join "`r`n"))

$response = Invoke-WebRequest -Uri $url -Method POST -ContentType "multipart/form-data; boundary=$boundary" -Body $body
$response.Content | ConvertFrom-Json | Select-Object status, image_url
```

Expected:
```json
{
  "status": "success",
  "image_url": "/uploads/1703046123_test.svg",
  "filename": "1703046123_test.svg"
}
```

**Uploaded files location**: `c:\smart_pg\backend\uploads\`

---

## 🤖 PART 2: CHATBOT TESTING

### 2.1 Chatbot Visibility
**Steps**:
1. Run frontend: http://localhost:3000
2. **Check**: 💬 button appears at **bottom-right** corner
3. All pages: Home, Results, Details, Login

**Expected**: Button visible on every page (fixed position)

### 2.2 Basic Chat Interaction
**Steps**:
1. Click 💬 button
2. Type: "Help"
3. **Check**: Bot responds with list of capabilities

**Response Should Include**:
- Find PGs by Budget
- Find by Location
- Find by Type (BHK)
- Find by Tenant Type
- Find Furnished PGs

### 2.3 Intent-Based Recommendations
**Test 1: Budget Search**
```
User: "Show me PGs under 10k"
Expected: Bot recognizes budget intent, searches for PGs ≤ ₹10,000
Shows top 5 matching PGs in chat
```

**Test 2: Location Search**
```
User: "PGs in Bangalore"
Expected: Filters by Bangalore city
Shows recommendations
```

**Test 3: Combined Filters**
```
User: "Show me 2BHK furnished PGs under 15k in Kolkata"
Expected: Extracts all entities and finds matching PGs
City: Kolkata
Budget: ₹15,000
BHK: 2
Furnishing: Furnished
```

**Test 4: Tenant Type**
```
User: "Bachelors friendly"
Expected: Shows PGs suitable for bachelors
```

### 2.4 Chat History
**Steps**:
1. Send multiple messages
2. Close chat (X button)
3. Reopen chat
4. **Check**: Previous messages are visible (localStorage)

**Expected**: Chat history persists during session

### 2.5 Recommendations Display in Chat
**Steps**:
1. Type: "Show me all PGs in Delhi"
2. **Check**: Bot response includes recommendation cards inside chat

**Card Format in Chat**:
```
🏢 Locality Name
₹Price/mo • X BHK
```

---

## 🔐 PART 3: GROQ API SETUP & INTEGRATION

### 3.1 Get Groq API Key
**Steps**:
1. Visit: https://console.groq.com
2. Sign up (free)
3. Create API key
4. Copy key

### 3.2 Configure .env File
**File**: `c:\smart_pg\backend\.env`

**Update**:
```bash
GROQ_API_KEY=your_actual_groq_api_key_here
GROQ_MODEL=mixtral-8x7b-32768
```

**Save file**

### 3.3 Restart Backend
```bash
# Kill previous Flask process (Ctrl+C in terminal)
# Then restart:
cd c:\smart_pg\backend
c:\smart_pg\venv\Scripts\python.exe app.py
```

### 3.4 Test Groq Integration
**Steps**:
1. Open chat (💬 button)
2. Type: "What PGs do you recommend for a startup professional?"
3. **Check**: Bot uses Groq API to generate thoughtful response
4. Response is more natural than simple keyword matching

**Expected Behavior**:
- ✅ Response is contextual and conversational
- ✅ If Groq API fails → fallback to basic recommendations
- ✅ No errors in console

**Verify API Communication**:
Check backend terminal for:
- Should NOT see "Groq API call failed"
- Should see normal chat processing

---

## 🎨 PART 4: UI ANIMATIONS & SKELETON LOADERS

### 4.1 PG Card Animations
**Steps**:
1. Load results page
2. Hover over PG card
3. **Check animations**:

**Expected Behaviors**:
- ✅ Card scales up smoothly (hover:scale-105)
- ✅ Card moves up slightly (hover:-translate-y-1)
- ✅ Shadow expands (hover:shadow-2xl)
- ✅ Image zooms when hovering over it
- ✅ Gradient overlay appears on image on hover
- ✅ "View Details" text appears on hover
- ✅ Button has gradient background
- ✅ Button scales on click

### 4.2 Image Overlay Gradient
**Steps**:
1. Go to Results page
2. Look at PG cards
3. Hover over image area
4. **Check**: Dark gradient overlay appears from bottom to top

**Expected**: Gradient transitions smoothly (opacity-0 → opacity-60)

### 4.3 Card Stagger Animation
**Steps**:
1. Load results page
2. **Check**: Cards appear one after another (not all at once)

**Expected**: Each card has slight delay in fade-in animation
(0ms, 50ms, 100ms, etc.)

### 4.4 Skeleton Loaders
**Note**: Skeleton loaders are implemented but visible only during actual loading.

**Trigger Skeleton Loader**:
1. Go to HomePage
2. Open browser DevTools (F12)
3. Network tab → Throttle to "Slow 3G"
4. Click "Get Recommendations"
5. **Check**: Grey shimmer placeholders appear while loading

**Expected Skeleton Layout**:
```
[Image Shimmer]
[Title Shimmer]
[Location Shimmer]
[Price Shimmer]
[Details Shimmer]
[Tags Shimmer]
[Button Shimmer]
```

---

## 🔄 PART 5: COMPLETE END-TO-END FLOW

### Scenario: Find PG and Save to Favorites

**Step 1: Register**
```
1. Go to http://localhost:3000/register
2. Fill:
   - Username: testuser1
   - Email: test1@example.com
   - Password: Test@123
3. Click Register
4. Should redirect to login page
```

**Step 2: Login**
```
1. Enter credentials from Step 1
2. Click Login
3. Expected: Redirects to home page, shows "Welcome, testuser1"
```

**Step 3: Search with Chat**
```
1. Click 💬 button
2. Type: "Show me 2BHK PGs under 20000 in Bangalore"
3. Chat bot shows recommendations with images
```

**Step 4: Search with Form**
```
1. In search form (home page):
   - City: Bangalore
   - Budget: ₹20,000
   - Tenant Type: Any
2. Click "Get Recommendations"
3. Results page shows PG cards with images and animations
```

**Step 5: View Details**
```
1. Click on any PG card
2. Details page shows:
   - Large image
   - All details (BHK, rent, amenities, etc.)
   - Similar PGs
3. Images load correctly
```

**Step 6: Test Fallback Image**
```
1. Open browser DevTools
2. Go to Application → Local Storage
3. Find any PG card's image_url
4. Manually change image URL to invalid path
5. Reload page
6. Expected: Fallback image (placeholder) shows instead of broken image
```

**Step 7: Test Chatbot Memory**
```
1. Send 3 messages via chat
2. Close chat (X button)
3. Reopen chat (💬 button)
4. Expected: Chat history still visible
```

---

## 📊 PART 6: DATABASE & API VERIFICATION

### 6.1 Verify Database Has Images
```bash
cd c:\smart_pg\backend
c:\smart_pg\venv\Scripts\python.exe -c "
from app import app, db
from models import PG

with app.app_context():
    pgs = PG.query.limit(5).all()
    for pg in pgs:
        print(f'{pg.area_locality}: {pg.image_url}')
"
```

**Expected Output**:
```
Bandel: /images/pg/pg_placeholder_2.svg
Whitefield: /images/pg/pg_placeholder_4.svg
...
```

### 6.2 Test All API Endpoints

**1. Health Check**:
```bash
Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing | Select-Object -ExpandProperty Content
```
Expected: `{"status": "ok", "message": "Smart PG Recommendation API is running"}`

**2. Get Cities**:
```bash
Invoke-WebRequest -Uri "http://localhost:5000/api/cities" -UseBasicParsing | Select-Object -ExpandProperty Content
```
Expected: List of 6 cities

**3. Get Recommendations with Images**:
```bash
Invoke-WebRequest -Uri "http://localhost:5000/api/recommend?city=Kolkata&max_budget=15000" -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json | Select-Object -ExpandProperty recommendations | Select-Object -First 1 | Select-Object area_locality, image_url
```
Expected: PG with image_url field populated

**4. Upload Image**:
```bash
# Already tested in Part 1.4
```

**5. Chat Message**:
```bash
$body = @{message="Show me PGs under 10k in Delhi"} | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:5000/api/chat/message" -Method POST -Headers @{"Content-Type"="application/json"} -Body $body -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json | Select-Object -ExpandProperty response
```
Expected: Response with recommendations or help message

---

## ✅ FINAL CHECKLIST

- [ ] Images display on PG cards
- [ ] Image fallback works (onError handler)
- [ ] Image overlay gradient appears on hover
- [ ] Card scales and moves on hover
- [ ] Button has smooth animations
- [ ] Chatbot visible on all pages
- [ ] Chatbot responds to intents
- [ ] Chat history persists
- [ ] Recommendations show in chat
- [ ] Groq API key configured (.env)
- [ ] Groq responses are natural/conversational
- [ ] Skeleton loaders appear during loading (with slow network)
- [ ] Card stagger animation works
- [ ] All API endpoints return correct data with image_url
- [ ] Database has image URLs assigned
- [ ] No console errors
- [ ] Responsive design works (mobile/tablet/desktop)

---

## 🚀 TROUBLESHOOTING

### Images Not Loading
```
1. Check if files exist:
   dir c:\smart_pg\frontend\public\images\pg\
   
2. Check image URL in browser DevTools:
   - Right-click image → Inspect
   - Check src attribute
   
3. Verify backend is serving images:
   http://localhost:5000/images/pg/pg_placeholder_1.svg
```

### Chatbot Not Responding
```
1. Check backend console for errors
2. Verify chat endpoint:
   POST http://localhost:5000/api/chat/message
   
3. Check CORS is enabled (should be)
```

### Groq API Not Working
```
1. Verify API key in .env:
   cat c:\smart_pg\backend\.env | findstr GROQ
   
2. Check if key is valid (visit console.groq.com)
3. Verify internet connection
4. Check backend logs for API errors
```

### Animations Not Showing
```
1. Clear browser cache (Ctrl+Shift+Delete)
2. Check CSS is loaded:
   - Open DevTools → Styles
   - Search for "hover:scale-105"
3. Verify Tailwind CSS is compiled
```

---

## 📚 KEY FILES REFERENCE

| Feature | File | Changes |
|---------|------|---------|
| Images | `frontend/public/images/pg/` | Created 5 placeholder SVGs |
| | `backend/load_data.py` | Assigns random images to PGs |
| | `backend/models.py` | `image_url` field already exists |
| Chatbot | `frontend/src/components/ChatBot.jsx` | Global component |
| | `backend/routes/chat_routes.py` | Groq API integration |
| Groq | `backend/.env` | API key configuration |
| | `backend/routes/chat_routes.py` | `call_groq_api()` function |
| UI | `frontend/src/pages/ResultsPage.jsx` | Card animations & overlays |
| | `frontend/src/components/Skeleton.jsx` | Skeleton loaders |
| | `frontend/src/index.css` | Animation definitions |
| Uploads | `backend/routes/upload_routes.py` | Image upload API |
| | `backend/app.py` | `/uploads/` route registered |

---

## 🎓 QUICK START

```bash
# 1. Stop any running servers
# 2. Update .env with Groq API key
# 3. Clear database (optional):
#    rm c:\smart_pg\backend\instance\database.db
# 4. Start backend:
cd c:\smart_pg\backend
c:\smart_pg\venv\Scripts\python.exe app.py

# 5. In new terminal, start frontend:
cd c:\smart_pg\frontend
npm start

# 6. Open http://localhost:3000
# 7. Test features as per testing guide above
```

---

**Last Updated**: April 29, 2026  
**Status**: ✅ All Features Implemented & Documented
