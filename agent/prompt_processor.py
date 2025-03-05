import json
import re
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.googlesearch import GoogleSearchTools
from config import GEMINI_API_KEY
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_json(raw_text: str) -> str:
    """
    Robustly extract a JSON array from raw_text.
    Uses a simple search for the first occurrence of a bracketed array.
    """
    try:
        match = re.search(r'\[.*\]', raw_text, re.DOTALL)
        if match:
            return match.group(0).strip()
        return "[]"
    except Exception as e:
        logger.error(f"Error extracting JSON: {e}")
        return "[]"

def process_prompt(user_prompt: str):
    """
    Processes the user prompt to generate a playlist recommendation.
    This version forces the agent to fetch live song data via the Google Search tool,
    and configures the search tool with specific parameters (fixed_max_results, fixed_language, timeout, etc.).
    """
    # Base instructions that force a live search call:
    base_instruction = """
    You are an expert music curator with real-time web access.
    BEFORE generating any song recommendations, you MUST use the provided Google Search tool 
    to look up the most recent song details. DO NOT rely on internal knowledge unless abosolutely necessary.
    Use the tool call command: "CALL GOOGLE SEARCH TOOL NOW:" followed by your query.
    """
    
    # Additional concise instructions:
    song_instructions = """
    Instructions:
    - Generate a curated playlist of exactly 20-25 songs.
    - For each song, output an object with exactly two keys: "name" (song title) and "artist" (primary artist).
    - Do not include any extra commentary.
    """
    
    # Combine all instructions into one description.
    description = base_instruction + "\n" + song_instructions

    try:
        # Create the GoogleSearchTools instance with specific parameters.
        # These parameters come from the documentation:
        # fixed_max_results: maximum number of search results,
        # fixed_language: language code, and timeout in seconds.
        search_tool = GoogleSearchTools(
            fixed_max_results=10,  # or any other value you prefer
            fixed_language="en",
            timeout=10  # seconds
        )

        # Create the agent with the search tool.
        agent = Agent(
            model=Gemini(
                api_key=GEMINI_API_KEY,
                id="gemini-2.0-flash-exp",
                temperature=0.1
            ),
            tools=[search_tool],
            description=description,
            markdown=True,
        )

        # Build an enhanced prompt with explicit step instructions.
        enhanced_prompt = f"""
        Given the user request: "{user_prompt}"
        FIRST: CALL GOOGLE SEARCH TOOL NOW: Search for current song details relevant to this query.
        THEN: Based solely on the live search results, generate a curated playlist of exactly 20-25 songs.
        Each song must be output as an object with keys "name" and "artist".
        Do not include any additional text.
        """

        response = agent.run(enhanced_prompt)
        json_text = extract_json(response.content)
        try:
            recommendations = json.loads(json_text)
            if len(recommendations) < 15:
                logger.warning(f"Generated only {len(recommendations)} recommendations. Expected at least 15.")
            logger.info(f"Generated {len(recommendations)} song recommendations")
            return recommendations
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}\nResponse Content: {json_text}")
            return []
    except Exception as e:
        logger.error(f"Error in prompt processing: {e}")
        return []

