import requests
import datetime
import time
from flask import Flask, jsonify

app = Flask(__name__)

# IFTTT Webhook URL
IFTTT_URL = "https://maker.ifttt.com/trigger/Play%20sound/with/key/cf_7Y_sYGjb85DLLGlUdlw"

def check_alarm_time(alarm_time):
    """Check if current time matches alarm time"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    return current_time == alarm_time

def check_all_false():
    """Check if all users have their alarms set to false"""
    try:
        response = requests.get("http://localhost:5000/api/check_all_false")
        if response.status_code == 200:
            return response.json().get("all_false", False)
    except requests.exceptions.RequestException:
        return False
    return False

def trigger_alarm():
    """Trigger the IFTTT webhook"""
    try:
        response = requests.post(IFTTT_URL)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def main():
    while True:
        try:
            # Get current alarm time
            response = requests.get("http://localhost:5000/api/get_alarm_time")
            if response.status_code == 200:
                alarm_time = response.json().get("alarm_time")
                
                if alarm_time and check_alarm_time(alarm_time):
                    print(f"Alarm time reached: {alarm_time}")
                    
                    # Keep triggering alarm until all users set their alarms to false
                    while not check_all_false():
                        if trigger_alarm():
                            print("Alarm triggered successfully")
                        else:
                            print("Failed to trigger alarm")
                        time.sleep(1)  # Wait 1 second between triggers
                    
                    print("All users have set their alarms to false")
            
            time.sleep(30)  # Check every 30 seconds
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            time.sleep(60)  # Wait longer on error

if __name__ == "__main__":
    print("Starting alarm checker...")
    main() 