from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alarm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Replace with a real secret key in production
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    alarm_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class AlarmTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alarm_time = db.Column(db.DateTime, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please provide both username and password')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please provide both username and password')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        try:
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash('Error during registration')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/api/set_alarm_time', methods=['POST'])
def set_alarm_time():
    try:
        time_str = request.json.get('time')
        if not time_str:
            return jsonify({'status': 'error', 'message': 'No time provided'}), 400
            
        try:
            alarm_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid time format'}), 400
        
        # Clear existing alarm time
        AlarmTime.query.delete()
        
        # Set new alarm time
        new_alarm = AlarmTime(alarm_time=alarm_time)
        db.session.add(new_alarm)
        
        # Reset all user alarms to active
        User.query.update({User.alarm_active: True})
        
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/toggle_alarm', methods=['POST'])
@login_required
def toggle_alarm():
    try:
        current_user.alarm_active = not current_user.alarm_active
        db.session.commit()
        return jsonify({'status': 'success', 'alarm_active': current_user.alarm_active})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/check_alarm_status', methods=['GET'])
def check_alarm_status():
    try:
        # Get all users and their alarm status
        users = User.query.all()
        user_states = {user.username: user.alarm_active for user in users}
        
        # Check if all users have their alarms active
        all_active = all(user.alarm_active for user in users) if users else False
        
        return jsonify({
            'all_active': all_active,
            'user_states': user_states
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/check_user_state', methods=['GET'])
@login_required
def check_user_state():
    try:
        return jsonify({
            'username': current_user.username,
            'alarm_active': current_user.alarm_active
        })
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

@app.route('/api/check_all_false', methods=['GET'])
def check_all_false():
    try:
        # Get all users
        users = User.query.all()
        
        # Check if all users have their alarms inactive (False)
        all_false = all(not user.alarm_active for user in users) if users else False
        
        return jsonify({'all_false': all_false})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 