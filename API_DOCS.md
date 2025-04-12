# Alarm System API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Set Alarm Time
Set the alarm time and reset all users' alarms to active.

**Endpoint:** `/api/set_alarm_time`  
**Method:** `POST`  
**Content-Type:** `application/json`

**Request Body:**
```json
{
    "time": "2024-03-20T15:30"  // Format: YYYY-MM-DDTHH:MM
}
```

**Response:**
```json
{
    "status": "success"
}
```

**Error Response:**
```json
{
    "status": "error",
    "message": "Error message here"
}
```

### 2. Toggle User Alarm
Toggle a specific user's alarm state.

**Endpoint:** `/api/toggle_alarm/<username>`  
**Method:** `POST`

**Response:**
```json
{
    "status": "success",
    "alarm_active": true/false
}
```

**Error Response:**
```json
{
    "status": "error",
    "message": "Error message here"
}
```

### 3. Check Alarm Status
Get the status of all alarms and users.

**Endpoint:** `/api/check_alarm_status`  
**Method:** `GET`

**Response:**
```json
{
    "all_active": true/false,
    "user_states": {
        "user1": true,
        "user2": false
    }
}
```

**Error Response:**
```json
{
    "status": "error",
    "message": "Error message here"
}
```

### 4. Check All False
Check if all users have their alarms set to false.

**Endpoint:** `/api/check_all_false`  
**Method:** `GET`

**Response:**
```json
{
    "all_false": true/false
}
```

**Error Response:**
```json
{
    "status": "error",
    "message": "Error message here"
}
```

### 5. Check User State
Get the alarm state of a specific user.

**Endpoint:** `/api/check_user_state/<username>`  
**Method:** `GET`

**Response:**
```json
{
    "username": "username",
    "alarm_active": true/false
}
```

**Error Response (User Not Found):**
```json
{
    "status": "error",
    "message": "User not found"
}
```

### 6. Get Alarm Time
Get the currently set alarm time.

**Endpoint:** `/api/get_alarm_time`  
**Method:** `GET`

**Response:**
```json
{
    "alarm_time": "2024-03-20T15:30"  // Format: YYYY-MM-DDTHH:MM
}
```

**Response (No Alarm Set):**
```json
{
    "alarm_time": null
}
```

### 7. User Registration
Register a new user.

**Endpoint:** `/api/register`  
**Method:** `POST`  
**Content-Type:** `application/json`

**Request Body:**
```json
{
    "username": "newuser",
    "password": "password123"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "User registered successfully"
}
```

**Error Response:**
```json
{
    "status": "error",
    "message": "Username already exists"
}
```

### 8. User Login
Authenticate a user and get a session token.

**Endpoint:** `/api/login`  
**Method:** `POST`  
**Content-Type:** `application/json`

**Request Body:**
```json
{
    "username": "username",
    "password": "password"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Login successful",
    "token": "session_token_here"
}
```

**Error Response:**
```json
{
    "status": "error",
    "message": "Invalid username or password"
}
```

### 9. User Logout
Logout the current user and invalidate the session.

**Endpoint:** `/api/logout`  
**Method:** `POST`

**Response:**
```json
{
    "status": "success",
    "message": "Logged out successfully"
}
```

## Example Usage

### Setting an Alarm
```bash
curl -X POST http://localhost:5000/api/set_alarm_time \
  -H "Content-Type: application/json" \
  -d '{"time": "2024-03-20T15:30"}'
```

### Toggling a User's Alarm
```bash
curl -X POST http://localhost:5000/api/toggle_alarm/john
```

### Checking if All Alarms are False
```bash
curl http://localhost:5000/api/check_all_false
```

### Checking a Specific User's State
```bash
curl http://localhost:5000/api/check_user_state/john
```

### Registering a New User
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser", "password": "password123"}'
```

### Logging In
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "username", "password": "password"}'
```

### Logging Out
```bash
curl -X POST http://localhost:5000/api/logout
```

## Notes
- All times are in 24-hour format
- User names are case-sensitive
- The alarm system requires all users to have their alarms set to false to turn off
- Setting a new alarm time automatically resets all users' alarms to active (true) 