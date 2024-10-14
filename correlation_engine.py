import os
from openai import OpenAI
import json
from models import Interview
from app import db

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_interviews():
    interviews = Interview.query.all()
    all_data = [json.loads(interview.data) for interview in interviews]

    prompt = f"""
    Analyze the following interview data from the AI datacenter market:
    {json.dumps(all_data, indent=2)}

    Please provide the following insights:
    1. Identify the top 3 market trends across all interviews.
    2. Find correlations between product offerings and market challenges.
    3. Analyze the competitive landscape and identify key players.
    4. Summarize the most significant technology advancements mentioned.
    5. Provide an overall market outlook based on the data.

    Format the response as a JSON object with the following structure:
    {{
        "market_trends": [string, string, string],
        "product_challenge_correlations": [string, string, string],
        "key_players": [string, string, string],
        "technology_advancements": [string, string, string],
        "market_outlook": string
    }}
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("OpenAI returned an empty response.")

    return json.loads(content)

def get_correlated_insights():
    try:
        insights = analyze_interviews()
        return insights
    except Exception as e:
        print(f"Error in correlation engine: {str(e)}")
        return None
