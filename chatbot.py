import os
from openai import OpenAI
from models import Interview
from app import db
import json

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_chatbot_response(user_input):
    # Fetch all interview data
    interviews = Interview.query.all()
    interview_data = [json.loads(interview.data) for interview in interviews]

    # Prepare the context for the chatbot
    context = f"""
    You are an AI Datacenter Analyst chatbot. You have access to the following interview data:
    {json.dumps(interview_data, indent=2)}
    
    Use this information to answer user queries about the AI datacenter market.
    If you don't have enough information to answer a question, say so and suggest what kind of data might help answer it in future interviews.
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in chatbot response: {str(e)}")
        return "I'm sorry, I encountered an error while processing your request. Please try again later."

def conduct_interview_chat(participant_type):
    missing_data = analyze_previous_interviews()
    conversation_history = []
    interview_data = {
        "product_offerings": [],
        "market_trends": [],
        "competitive_landscape": [],
        "technology_advancements": [],
        "future_outlook": []
    }

    # Generate initial questions
    questions = generate_dynamic_questions(participant_type, missing_data)
    
    for question in questions:
        conversation_history.append({"role": "assistant", "content": question})
        yield {"role": "assistant", "content": question}

        # Wait for user response
        user_response = yield

        conversation_history.append({"role": "user", "content": user_response})

        # Process the response and update interview_data
        process_response(user_response, interview_data)

    # Final analysis and summary
    summary_prompt = f"""
    Based on the following conversation, provide a summary of the interview:
    {json.dumps(conversation_history, indent=2)}

    Summarize the key points for each of these categories:
    1. Product offerings
    2. Market trends
    3. Competitive landscape
    4. Technology advancements
    5. Future outlook

    Provide the summary in a structured JSON format with these categories.
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": summary_prompt}],
        response_format={"type": "json_object"},
    )

    summary = json.loads(response.choices[0].message.content)
    
    # Merge summary with existing interview_data
    for category in interview_data.keys():
        interview_data[category].extend(summary.get(category, []))

    return json.dumps(interview_data)

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

def process_response(user_response, interview_data):
    prompt = f"""
    Analyze the following user response and categorize the information into these categories:
    1. Product offerings
    2. Market trends
    3. Competitive landscape
    4. Technology advancements
    5. Future outlook

    User response: {user_response}

    Provide the categorized information in a JSON format with these categories as keys and lists of extracted information as values.
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        categorized_data = json.loads(response.choices[0].message.content)
        
        for category, items in categorized_data.items():
            interview_data[category].extend(items)
    except Exception as e:
        print(f"Error processing response: {str(e)}")

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