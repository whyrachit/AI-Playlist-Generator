"""
prompt_processor.py - Agent logic for processing user prompts using Agno and Groq's model.

This module defines a function that leverages Agno’s agent framework with the Groq model
to extract details from the user's natural language prompt and generate an initial list of 
song recommendations in JSON format.
"""

import json
import re
from agno.agent import Agent
from agno.models.groq import Groq
from config import GROQ_API_KEY

def extract_json(raw_text: str) -> str:
    """
    Extracts a JSON array from the raw_text using a regex pattern.
    
    Args:
        raw_text (str): The raw text output from the agent.
    
    Returns:
        str: The extracted JSON string, or an empty string if no JSON array is found.
    """
    match = re.search(r'(\[.*\])', raw_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def process_prompt(user_prompt: str):
    """
    Processes the user's prompt using Agno's agent framework with Groq's model.
    
    The agent is tasked to act as a professional music playlist curator. It extracts relevant details
    from the prompt and returns a list of 30 song recommendations. Each recommendation is expected to be 
    a JSON object with exactly two keys: "name" and "artist". The output must be a valid JSON array and 
    nothing else.
    
    Args:
        user_prompt (str): The natural language prompt entered by the user.
    
    Returns:
        list: A list of song recommendation dictionaries. Returns an empty list if parsing fails.
    """
    description = ("""
        You are a professional music playlist curator with a deep understanding of diverse genres, eras, and moods. 
        Your task is to create a curated list of 30 unique song recommendations (if feasible) based on the provided prompt. 
        Each song should be thoughtfully selected to ensure a well-balanced and engaging playlist that appeals to a wide range of musical tastes.
        Your output must be a JSON array where each element is a JSON object containing exactly two keys:
        "name": A string representing the title of the song.
        "artist": A string representing the performing artist's name.
        Do not include any extra keys or fields beyond "name" and "artist".
        Return only the JSON array without any additional text, explanations, or formatting tags.
        Based on the given prompt, generate your list of 30 song recommendations strictly following these instructions.
    """)
    
    # Initialize the agent with the Groq model. (Replace with your Groq API key if needed.)
    agent = Agent(
        model=Groq(api_key=GROQ_API_KEY, id="deepseek-r1-distill-llama-70b"),
        description=description,
        markdown=True
    )
    
    response = agent.run(user_prompt)
    json_text = extract_json(response.content)
    
    try:
        recommendations = json.loads(json_text)
    except json.JSONDecodeError:
        recommendations = []
    
    return recommendations
