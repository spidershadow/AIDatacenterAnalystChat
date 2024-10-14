from flask import render_template, request, redirect, url_for, jsonify, flash, session
from app import app, db
from models import Interview
from interview_ai import conduct_interview, analyze_previous_interviews
from correlation_engine import get_correlated_insights
from chatbot import get_chatbot_response, conduct_interview_chat
from market_model import update_market_model, add_interview_to_model, get_market_model_summary, get_category_data
from datetime import datetime
import json

@app.route('/')
def index():
    return render_template('interview.html')

@app.route('/dashboard')
def dashboard():
    interviews = Interview.query.all()
    return render_template('dashboard.html', interviews=interviews)

@app.route('/interview', methods=['GET', 'POST'])
def interview():
    if request.method == 'POST':
        participant_type = request.form['participant_type']
        company_name = request.form['company_name']
        
        try:
            missing_data_before = analyze_previous_interviews()
            app.logger.info(f"Missing data points before interview: {missing_data_before}")
            
            interview_data = conduct_interview(participant_type)
            
            app.logger.info(f"Interview data: {interview_data}")
            
            new_interview = Interview(
                participant_type=participant_type,
                company_name=company_name,
                data=interview_data,
                completed=True
            )
            
            db.session.add(new_interview)
            db.session.commit()
            
            # Update market model with new interview data
            add_interview_to_model(new_interview)
            
            missing_data_after = analyze_previous_interviews()
            app.logger.info(f"Missing data points after interview: {missing_data_after}")
            
            flash('Interview conducted successfully!', 'success')
            return redirect(url_for('dashboard'))
        except ValueError as e:
            app.logger.error(f"Error during interview: {str(e)}")
            flash(str(e), 'error')
        except Exception as e:
            app.logger.error(f"Unexpected error during interview: {str(e)}")
            flash('An unexpected error occurred while conducting the interview. Please try again.', 'error')
    
    return render_template('interview.html')

@app.route('/api/interview_data')
def get_interview_data():
    interviews = Interview.query.all()
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

@app.route('/insights')
def insights():
    correlated_insights = get_correlated_insights()
    return render_template('insights.html', insights=correlated_insights)

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_input = request.form['user_input']
        response = get_chatbot_response(user_input)
        return jsonify({'response': response})
    return render_template('chatbot.html')

@app.route('/interview_chat', methods=['GET', 'POST'])
def interview_chat():
    if request.method == 'GET':
        return render_template('interview_chat.html')
    
    participant_type = request.form.get('participant_type')
    company_name = request.form.get('company_name')
    user_input = request.form.get('user_input')

    if 'interview' not in session:
        session['interview'] = conduct_interview_chat(participant_type)
        session['company_name'] = company_name
        next(session['interview'])  # Initialize the generator

    try:
        response = session['interview'].send(user_input)
        
        if isinstance(response, str):  # Interview is complete
            new_interview = Interview(
                participant_type=participant_type,
                company_name=session['company_name'],
                data=response,
                completed=True
            )
            db.session.add(new_interview)
            db.session.commit()
            
            # Update market model with new interview data
            add_interview_to_model(new_interview)
            
            session.pop('interview', None)
            session.pop('company_name', None)
            return jsonify({'status': 'complete', 'message': 'Interview completed successfully!'})
        else:
            return jsonify({'status': 'ongoing', 'message': response['content']})
    except StopIteration:
        session.pop('interview', None)
        session.pop('company_name', None)
        return jsonify({'status': 'error', 'message': 'Interview ended unexpectedly.'})

@app.route('/market_model')
def market_model():
    model_summary = get_market_model_summary()
    return render_template('market_model.html', model_summary=model_summary)

@app.route('/api/market_model/<category>')
def api_market_model_category(category):
    category_data = get_category_data(category)
    return jsonify(category_data)

@app.route('/api/market_model_summary')
def api_market_model_summary():
    model_summary = get_market_model_summary()
    return jsonify(model_summary)

@app.before_request
def update_model():
    update_market_model()
