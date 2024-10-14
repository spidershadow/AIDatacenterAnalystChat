import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def conduct_interview(participant_type):
    prompt = f"""
    Conduct a focused 10-15 minute interview with a {participant_type} in the AI datacenter market.
    Extract and summarize key information related to:
    1. Current product offerings and roadmap
    2. Market trends and challenges
    3. Competitive landscape
    4. Technology advancements
    5. Future outlook and strategy
    
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

