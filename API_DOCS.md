# API Documentation

Quick reference for all available endpoints.

## Authentication Endpoints

### Register
```
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password_123"
}

Response:
{
  "status": "success",
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password_123"
}

Response:
{
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": { ... }
}
```

### Verify Token
```
GET /api/auth/verify-token
Authorization: Bearer <token>

Response:
{
  "status": "success",
  "user": { ... }
}
```

---

## Recommendation Endpoints

### Get Recommendations
```
GET /api/recommend?city=Bangalore&max_budget=15000&tenant_type=Bachelors&top_n=5

Response:
{
  "status": "success",
  "count": 5,
  "recommendations": [
    {
      "id": 1,
      "bhk": 2,
      "rent": 12000,
      "area_locality": "Whitefield",
      "city": "Bangalore",
      "furnishing_status": "Semi-Furnished",
      "rating": 4.5,
      "image_url": "..."
    }
  ]
}
```

### Get PG Details
```
GET /api/pg/1

Response:
{
  "status": "success",
  "pg": {
    "id": 1,
    "bhk": 2,
    "rent": 12000,
    "area_locality": "Whitefield",
    "amenities": [
      { "name": "WiFi", "available": true },
      { "name": "Parking", "available": true }
    ],
    "reviews": [
      { "user": "ram", "rating": 5.0, "comment": "Great place!" }
    ],
    "similar_pgs": [ ... ]
  }
}
```

### Filter PGs
```
GET /api/filter?city=Bangalore&min_budget=5000&max_budget=20000&bhk=2&furnishing=Furnished

Response:
{
  "status": "success",
  "total": 25,
  "pgs": [ ... ]
}
```

### Get All Cities
```
GET /api/cities

Response:
{
  "status": "success",
  "cities": ["Bangalore", "Kolkata", "Delhi", ...]
}
```

### Get Localities by City
```
GET /api/localities/Bangalore

Response:
{
  "status": "success",
  "city": "Bangalore",
  "localities": ["Whitefield", "Koramangala", "JP Nagar", ...]
}
```

### Get Statistics
```
GET /api/stats

Response:
{
  "status": "success",
  "stats": {
    "total_pgs": 250,
    "average_rent": 15000,
    "average_rating": 4.2
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "status": "error",
  "message": "Missing required fields"
}
```

### 401 Unauthorized
```json
{
  "status": "error",
  "message": "Invalid token"
}
```

### 404 Not Found
```json
{
  "status": "error",
  "message": "PG not found"
}
```

### 500 Server Error
```json
{
  "status": "error",
  "message": "Internal server error"
}
```

---

## Query Parameters

| Parameter | Type | Example | Description |
|-----------|------|---------|-------------|
| city | string | Bangalore | City name |
| max_budget | integer | 20000 | Maximum monthly rent |
| min_budget | integer | 5000 | Minimum monthly rent |
| tenant_type | string | Bachelors | Bachelors, Family, Any |
| bhk | integer | 2 | Number of bedrooms |
| furnishing | string | Furnished | Furnished, Semi-Furnished, Unfurnished |
| area_type | string | Super Area | Super Area, Carpet Area |
| top_n | integer | 5 | Number of results |
| skip | integer | 0 | For pagination |
| limit | integer | 20 | Records per page |

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Server Error |

---

## Authentication

Include JWT token in Authorization header:

```
Authorization: Bearer <token>
```

Where `<token>` is obtained from login endpoint.

---

## CORS Headers

The API supports CORS for frontend development:
- Allowed Origins: http://localhost:3000, http://localhost:5000
- Allowed Methods: GET, POST, PUT, DELETE, OPTIONS
- Allowed Headers: Content-Type, Authorization
