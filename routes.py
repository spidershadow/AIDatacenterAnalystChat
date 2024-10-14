from flask import render_template, request, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, login_manager
from models import User, Interview
from interview_ai import conduct_interview
from correlation_engine import get_correlated_insights
from datetime import datetime
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(username=request.form['username'], email=request.form['email'])
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    interviews = Interview.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', interviews=interviews)

@app.route('/interview', methods=['GET', 'POST'])
@login_required
def interview():
    if request.method == 'POST':
        participant_type = request.form['participant_type']
        company_name = request.form['company_name']
        
        interview_data = conduct_interview(participant_type, current_user.id)
        
        new_interview = Interview(
            participant_type=participant_type,
            company_name=company_name,
            interview_date=datetime.utcnow(),
            user_id=current_user.id,
            data=interview_data,
            completed=True
        )
        
        db.session.add(new_interview)
        db.session.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('interview.html')

@app.route('/api/interview_data')
@login_required
def get_interview_data():
    interviews = Interview.query.filter_by(user_id=current_user.id).all()
    data = [
        {
            'id': interview.id,
            'participant_type': interview.participant_type,
            'company_name': interview.company_name,
            'interview_date': interview.interview_date.isoformat(),
            'data': interview.data,
            'completed': interview.completed
        }
        for interview in interviews
    ]
    return jsonify(data)

@app.route('/insights')
@login_required
def insights():
    correlated_insights = get_correlated_insights()
    return render_template('insights.html', insights=correlated_insights)
