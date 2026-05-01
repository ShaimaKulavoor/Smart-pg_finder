# 🚀 QUICK REFERENCE - TESTING CHECKLIST

## Pre-Flight Checklist

```bash
# 1. Backend .env configured?
cat c:\smart_pg\backend\.env | findstr GROQ_API_KEY
# Should show: GROQ_API_KEY=your_groq_api_key_here

# 2. Database has images?
c:\smart_pg\venv\Scripts\python.exe -c "
from backend.app import app
from backend.models import PG
with app.app_context():
    pg = PG.query.first()
    print(f'✅ Image: {pg.image_url}')
"

# 3. Start Backend
cd c:\smart_pg\backend
c:\smart_pg\venv\Scripts\python.exe app.py
# Expected: Running on http://127.0.0.1:5000

# 4. Start Frontend (new terminal)
cd c:\smart_pg\frontend
npm start
# Expected: Compiled successfully / compiled with warnings
```

---

## 5-Minute Test Sequence

### ✅ Test 1: Images Load (1 min)
```
1. Go to http://localhost:3000
2. Click "Get Recommendations"
3. Check: Images appear in cards
```

### ✅ Test 2: Chatbot Responds (1 min)
```
1. Click 💬 button (bottom-right)
2. Type: "Help"
3. Check: Bot lists capabilities
```

### ✅ Test 3: Chat Search (1 min)
```
1. Type in chat: "Show me PGs under 10k in Bangalore"
2. Check: Bot shows recommendations in chat
```

### ✅ Test 4: UI Animations (1 min)
```
1. Hover over PG card on results page
2. Check: Card scales up, shadow expands
3. Check: "View Details" text appears on image
```

### ✅ Test 5: Groq AI Response (1 min)
```
1. Type in chat: "What's your recommendation?"
2. Check: Natural language response (not just keywords)
3. If no response: Groq API not configured
```

---

## Feature-by-Feature Quick Test

### 📸 IMAGES
```bash
# Quick test
curl http://localhost:5000/api/recommend?city=Kolkata&max_budget=15000 | findstr image_url

# Expected: "image_url": "/images/pg/pg_placeholder_X.svg"
```

### 🤖 CHATBOT
```bash
# Test intent recognition
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"2BHK under 15k\"}"

# Expected: Extracts BHK=2, budget=15000, shows recommendations
```

### 🧠 GROQ API
```bash
# Verify API key loaded
# In backend terminal, should NOT show: "Groq API call failed"

# Test conversation
# Type in chat: "Suggest me a good PG for professionals"
# Should see thoughtful response (not just data)
```

### 🎨 ANIMATIONS
```
1. Open http://localhost:3000/results
2. Observe: Cards fade in sequentially
3. Hover card: Scales up 5%, shadow grows, image zooms
4. Hover image: Gradient overlay appears
5. Click button: Smooth transitions
```

### ⚡ SKELETON LOADER
```
1. Open DevTools (F12)
2. Network → Throttle to "Slow 3G"
3. Click "Get Recommendations"
4. Observe: Grey shimmer boxes before images load
```

---

## API Quick Tests

```bash
# 1. Health Check
curl http://localhost:5000/health

# 2. Get Cities
curl http://localhost:5000/api/cities

# 3. Get Recommendations (with images!)
curl "http://localhost:5000/api/recommend?city=Kolkata&max_budget=15000"

# 4. Chat (will use Groq API if configured)
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Show me PGs under 10k\"}"

# 5. Chat Suggestions
curl http://localhost:5000/api/chat/suggestions

# 6. Upload Image
# See TESTING_GUIDE.md for multipart upload example
```

---

## Troubleshooting Quick Fixes

| Issue | Fix |
|-------|-----|
| Images not loading | Check: `/frontend/public/images/pg/` exists? |
| Chatbot not responding | Check: Backend console for errors |
| Groq API not working | Update .env GROQ_API_KEY and restart backend |
| Animations not smooth | Clear cache: Ctrl+Shift+Delete in browser |
| Database empty | Run: `python backend/load_data.py` |
| Port 5000 in use | Kill process: `Get-Process python \| Stop-Process` |

---

## File Locations Reference

```
IMAGES:          c:\smart_pg\frontend\public\images\pg\
CHATBOT:         c:\smart_pg\frontend\src\components\ChatBot.jsx
GROQ CONFIG:     c:\smart_pg\backend\.env
UPLOAD API:      c:\smart_pg\backend\routes\upload_routes.py
ANIMATIONS:      c:\smart_pg\frontend\src\pages\ResultsPage.jsx
SKELETON:        c:\smart_pg\frontend\src\components\Skeleton.jsx
TESTING GUIDE:   c:\smart_pg\TESTING_GUIDE.md
```

---

## Expected Behaviors

### ✅ Images
- Display in PG cards ✓
- Fallback if broken ✓
- Zoom on hover ✓
- Overlay gradient ✓

### ✅ Chatbot
- Visible on all pages ✓
- Responds to intents ✓
- Shows recommendations ✓
- History persists ✓

### ✅ Groq
- Uses API if key present ✓
- Falls back to basic if no key ✓
- Natural language responses ✓
- No errors in console ✓

### ✅ UI
- Card hovers smoothly ✓
- Image zooms on hover ✓
- Buttons animate ✓
- Loading states show ✓

---

## Success Indicators

```
✅ Images appear on PG cards
✅ Chatbot responds to "help" command
✅ Chat searches find recommendations
✅ Cards scale on hover
✅ Image has dark overlay on hover
✅ Groq responses are conversational
✅ No console errors
✅ Skeleton loaders show (on slow network)
✅ All 6 cities appear in dropdown
✅ 4746 PGs in database
```

---

## Common Commands

```bash
# Check backend status
curl http://localhost:5000/health

# View logs
Get-Content c:\smart_pg\backend\instance\database.db

# Restart services
# Kill: Ctrl+C in terminals
# Restart: python app.py (backend), npm start (frontend)

# Clear cache
# Browser: Ctrl+Shift+Delete
# npm: npm cache clean --force

# Database query
python -c "from backend.app import app; from backend.models import PG; app.app_context().push(); print(PG.query.count())"
```

---

**⏱️ Estimated Testing Time: 15-20 minutes**  
**👤 Required: Groq API Key (free from console.groq.com)**  
**✨ Status: Ready to Test**
