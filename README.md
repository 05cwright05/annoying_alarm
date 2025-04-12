# Alarm System

A Flask-based alarm system that allows multiple users to manage and control alarms.

## Features

- Set a single alarm time for all users
- Individual user alarm control
- Web-based UI for easy management
- Real-time alarm status updates
- Alarm only turns off when all users have acknowledged

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## How to Use

1. **Set Alarm Time**:
   - Use the datetime picker to select when the alarm should go off
   - Click "Set Alarm" to save the time

2. **Add Users**:
   - Click the "Add User" button
   - Enter a username when prompted

3. **Control Alarms**:
   - Each user can toggle their alarm status using the "Toggle Alarm" button
   - The alarm will only turn off when all users have toggled their alarms off

## API Endpoints

- `POST /api/set_alarm_time`: Set the alarm time
- `POST /api/toggle_alarm/<username>`: Toggle a user's alarm status
- `GET /api/check_alarm_status`: Check if all alarms are active
- `GET /api/get_alarm_time`: Get the current alarm time 


https://maker.ifttt.com/trigger/Play%20sound/with/key/cf_7Y_sYGjb85DLLGlUdlw
