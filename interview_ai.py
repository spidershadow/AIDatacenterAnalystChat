import os
from openai import OpenAI
from models import Interview
from app import db
import json

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_previous_interviews():
    previous_interviews = Interview.query.all()
    all_data = [json.loads(interview.data) for interview in previous_interviews]
    
    missing_data = {
        "product_offerings": set(),
        "market_trends": set(),
        "competitive_landscape": set(),
        "technology_advancements": set(),
        "future_outlook": set()
    }
    
    for data in all_data:
        for category in missing_data.keys():
            if not data.get(category) or len(data[category]) < 2:
                missing_data[category].add(category)
    
    return missing_data

def generate_dynamic_questions(participant_type, missing_data):
    prompt = f"""
    As an AI interviewer, create a set of 5-7 focused questions for a {participant_type} in the AI datacenter market.
    The questions should be tailored to gather comprehensive information, especially on the following topics that are currently lacking in our data:
    {', '.join([k.replace('_', ' ').title() for k, v in missing_data.items() if v])}

    For each question:
    1. Make it specific to the {participant_type}'s role in the AI datacenter ecosystem.
    2. Phrase it to encourage detailed responses.
    3. Focus on extracting actionable insights and forward-looking perspectives.

    Format the response as a JSON array of strings, where each string is a complete question.
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        questions = json.loads(response.choices[0].message.content)
        return questions.get("questions", [])
    except Exception as e:
        print(f"Error generating questions: {str(e)}")
        return []

def conduct_interview(participant_type):
    missing_data = analyze_previous_interviews()
    questions = generate_dynamic_questions(participant_type, missing_data)
    
    if not questions:
        raise ValueError("Failed to generate interview questions.")
    
    interview_prompt = f"""
    Conduct a focused interview with a {participant_type} in the AI datacenter market.
    Use the following questions as a guide, but feel free to ask follow-up questions or explore relevant tangents:

    {json.dumps(questions, indent=2)}

    Extract and summarize key information related to:
    1. Current product offerings and roadmap
    2. Market trends and challenges
    3. Competitive landscape
    4. Technology advancements
    5. Future outlook and strategy

    Provide the response in a structured JSON format with these categories, ensuring comprehensive coverage of each topic.
    """
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": interview_prompt}],
            response_format={"type": "json_object"},
        )
        
        content = response.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned an empty response.")
        
        interview_data = json.loads(content)
        
        # Add the questions used to the interview data
        interview_data["questions_asked"] = questions
        
        return json.dumps(interview_data)
    except Exception as e:
        print(f"Error conducting interview: {str(e)}")
        raise ValueError(f"Failed to conduct interview: {str(e)}")
