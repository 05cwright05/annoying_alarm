import requests
import datetime
import time
import pygame
import sys
import os
import numpy as np

def check_alarm_time(alarm_time):
    """Check if current time matches alarm time"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    print(f"Current time: {current_time}, Alarm time: {alarm_time}")
    return current_time == alarm_time

def check_all_false():
    """Check if all users have their alarms set to false"""
    try:
        response = requests.get("http://localhost:5000/api/check_all_false")
        if response.status_code == 200:
            all_false = response.json().get("all_false", False)
            print(f"All false status: {all_false}")
            return all_false
    except requests.exceptions.RequestException as e:
        print(f"Error checking all false: {e}")
    return False

def generate_beep(frequency=440, duration=500, volume=0.5):
    """Generate a beep sound using numpy"""
    sample_rate = 44100
    t = np.linspace(0, duration/1000, int(sample_rate * duration/1000), False)
    wave = np.sin(2 * np.pi * frequency * t)
    wave = wave * volume
    wave = np.int16(wave * 32767)
    return wave

def initialize_pygame():
    """Initialize pygame mixer for sound playback"""
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=1)
        print("Sound system initialized...")
        return True
    except Exception as e:
        print(f"Error initializing sound system: {e}")
        return False

def play_alarm():
    """Play the alarm sound"""
    try:
        if not pygame.mixer.get_init():
            if not initialize_pygame():
                return
        
        # Generate and play the beep sound
        beep_sound = generate_beep()
        sound = pygame.sndarray.make_sound(beep_sound)
        sound.play()
        print("Playing alarm sound...")
    except Exception as e:
        print(f"Error playing sound: {e}")

def main():
    print("Starting alarm system...")
    print("Waiting for alarm time...")
    
    # Initialize pygame mixer
    initialize_pygame()
    
    try:
        while True:
            # Get current alarm time
            response = requests.get("http://localhost:5000/api/get_alarm_time")
            if response.status_code == 200:
                alarm_time = response.json().get("alarm_time")
                print(f"Current alarm time set to: {alarm_time}")
                
                if alarm_time and check_alarm_time(alarm_time):
                    print("Alarm time reached! Starting alarm...")
                    
                    # Keep playing alarm until all users set their alarms to false
                    while not check_all_false():
                        play_alarm()
                        time.sleep(1)  # Wait 1 second between plays
                    
                    print("All users have set their alarms to false")
                    break
                else:
                    print("Not yet alarm time...")
            
            time.sleep(30)  # Check every 30 seconds
            
    except KeyboardInterrupt:
        print("\nStopping alarm...")
        # Check one last time if all are false
        if not check_all_false():
            print("Warning: Not all users have set their alarms to false!")
            print("Alarm will continue playing...")
            main()  # Restart the alarm if not all are false
        else:
            print("All users have set their alarms to false. Alarm stopped.")

if __name__ == "__main__":
    main() 