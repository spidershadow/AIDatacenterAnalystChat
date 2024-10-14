from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, login_manager
from models import User, Interview
from interview_ai import conduct_interview, analyze_previous_interviews
from correlation_engine import get_correlated_insights
from datetime import datetime
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('interview.html')

@app.route('/admin')
@login_required
def admin():
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        user = User(username=request.form['username'], email=request.form['email'])
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('admin_login'))
    return render_template('register.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    interviews = Interview.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', interviews=interviews)

@app.route('/interview', methods=['GET', 'POST'])
def interview():
    if request.method == 'POST':
        participant_type = request.form['participant_type']
        company_name = request.form['company_name']
        
        try:
            user_id = current_user.id if current_user.is_authenticated else None
            
            # Log missing data points before the interview
            missing_data_before = analyze_previous_interviews(user_id)
            app.logger.info(f"Missing data points before interview: {missing_data_before}")
            
            interview_data = conduct_interview(participant_type, user_id)
            
            # Log the interview data to verify dynamic adjustment
            app.logger.info(f"Interview data: {interview_data}")
            
            new_interview = Interview(
                participant_type=participant_type,
                company_name=company_name,
                interview_date=datetime.utcnow(),
                user_id=user_id,
                data=interview_data,
                completed=True
            )
            
            db.session.add(new_interview)
            db.session.commit()
            
            # Log missing data points after the interview
            missing_data_after = analyze_previous_interviews(user_id)
            app.logger.info(f"Missing data points after interview: {missing_data_after}")
            
            flash('Interview conducted successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            app.logger.error(f"Error during interview: {str(e)}")
            flash('An error occurred while conducting the interview. Please try again.', 'error')
    
    return render_template('interview.html')

@app.route('/admin/api/interview_data')
@login_required
def get_interview_data():
    interviews = Interview.query.filter_by(user_id=current_user.id).all()
    data = [
        {
            'id': interview.id,
            'participant_type': interview.participant_type,
            'company_name': interview.company_name,
            'interview_date': interview.interview_date.isoformat(),
            'data': json.loads(interview.data),
            'completed': interview.completed
        }
        for interview in interviews
    ]
    return jsonify(data)

@app.route('/admin/insights')
@login_required
def insights():
    correlated_insights = get_correlated_insights()
    return render_template('insights.html', insights=correlated_insights)
