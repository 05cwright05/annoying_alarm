from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alarm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class AlarmTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alarm_time = db.Column(db.DateTime, nullable=False)

class UserAlarm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    alarm_active = db.Column(db.Boolean, default=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/set_alarm_time', methods=['POST'])
def set_alarm_time():
    try:
        time_str = request.json.get('time')
        alarm_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M')
        
        # Clear existing alarm time
        AlarmTime.query.delete()
        
        # Set new alarm time
        new_alarm = AlarmTime(alarm_time=alarm_time)
        db.session.add(new_alarm)
        
        # Reset all user alarms to active
        UserAlarm.query.update({UserAlarm.alarm_active: True})
        
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/toggle_alarm/<username>', methods=['POST'])
def toggle_alarm(username):
    try:
        user = UserAlarm.query.filter_by(username=username).first()
        if not user:
            user = UserAlarm(username=username, alarm_active=True)
            db.session.add(user)
        
        user.alarm_active = not user.alarm_active
        db.session.commit()
        return jsonify({'status': 'success', 'alarm_active': user.alarm_active})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/check_alarm_status', methods=['GET'])
def check_alarm_status():
    try:
        # Get all users and their alarm status
        users = UserAlarm.query.all()
        user_states = {user.username: user.alarm_active for user in users}
        
        # Check if all users have their alarms active
        all_active = all(user.alarm_active for user in users) if users else False
        
        return jsonify({
            'all_active': all_active,
            'user_states': user_states
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/check_all_false', methods=['GET'])
def check_all_false():
    try:
        # Get all users
        users = UserAlarm.query.all()
        
        # Check if all users have their alarms inactive (False)
        all_false = all(not user.alarm_active for user in users) if users else False
        
        return jsonify({'all_false': all_false})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/check_user_state/<username>', methods=['GET'])
def check_user_state(username):
    try:
        user = UserAlarm.query.filter_by(username=username).first()
        if user:
            return jsonify({
                'username': username,
                'alarm_active': user.alarm_active
            })
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/get_alarm_time', methods=['GET'])
def get_alarm_time():
    try:
        alarm = AlarmTime.query.first()
        if alarm:
            return jsonify({'alarm_time': alarm.alarm_time.strftime('%Y-%m-%dT%H:%M')})
        return jsonify({'alarm_time': None})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 