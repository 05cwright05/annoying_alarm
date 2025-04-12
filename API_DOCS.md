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

## Notes
- All times are in 24-hour format
- User names are case-sensitive
- The alarm system requires all users to have their alarms set to false to turn off
- Setting a new alarm time automatically resets all users' alarms to active (true) 