import os
from openai import OpenAI
from models import Interview
from app import db
import json

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_previous_interviews(user_id):
    previous_interviews = Interview.query.filter_by(user_id=user_id).all()
    all_data = [json.loads(interview.data) for interview in previous_interviews]
    
    # Identify missing data points
    missing_data = {
        "product_offerings": set(),
        "market_trends": set(),
        "competitive_landscape": set(),
        "technology_advancements": set(),
        "future_outlook": set()
    }
    
    for data in all_data:
        for category in missing_data.keys():
            if not data.get(category):
                missing_data[category].add(category)
    
    return missing_data

def conduct_interview(participant_type, user_id):
    missing_data = analyze_previous_interviews(user_id)
    
    prompt = f"""
    Conduct a focused 10-15 minute interview with a {participant_type} in the AI datacenter market.
    Extract and summarize key information related to:
    1. Current product offerings and roadmap
    2. Market trends and challenges
    3. Competitive landscape
    4. Technology advancements
    5. Future outlook and strategy
    
    Additionally, focus on the following missing data points from previous interviews:
    {', '.join([f"{k.replace('_', ' ').title()}" for k, v in missing_data.items() if v])}
    
    Provide the response in a structured JSON format with these categories.
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    
    content = response.choices[0].message.content
    if not content:
        raise ValueError("OpenAI returned an empty response.")
    
    return content
