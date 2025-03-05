import json
import re
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.googlesearch import GoogleSearchTools
from config import GROQ_API_KEY
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_json(raw_text: str) -> str:
    """
    Extract a JSON array from raw_text. If multiple arrays are present,
    choose the one that seems most complete. Fallback to empty array if extraction fails.
    """
    try:
        matches = re.findall(r'(\[.*\])', raw_text, re.DOTALL)
        if matches:
            # Optionally, choose the longest match assuming that is the complete JSON.
            best_match = max(matches, key=len)
            return best_match.strip()
        return "[]"
    except Exception as e:
        logger.error(f"Error extracting JSON: {e}")
        return "[]"

def process_prompt(user_prompt: str):
    """
    Processes the user prompt to generate a playlist recommendation.
    This function uses an LLM (with Google search integration for context) to extract structured song data.
    """
    description = """
    You are an expert music curator with deep knowledge across all genres and eras.
    Create a carefully curated playlist of 15-20 songs that perfectly match the user's prompt.

    Important guidelines:
    1. Focus on song diversity and flow.
    2. Include both popular and lesser-known tracks.
    3. Ensure genre consistency.
    4. Consider the emotional context.

    For each song, provide:
    - "name": Exact song title.
    - "artist": Primary artist name.

    Do not provide Spotify IDs; the backend will use Spotify's API to retrieve the official track IDs.
    
    Return only a valid JSON array with these exact fields.
    """

    try:
        # Initialize agent with enhanced configuration.
        agent = Agent(
            model=Groq(
                api_key=GROQ_API_KEY,
                id="deepseek-r1-distill-llama-70b",
                temperature=0.7,  # Balancing creativity and relevance.
                max_tokens=2000   # Provide enough context for detailed responses.
            ),
            tools=[GoogleSearchTools()],
            description=description,
            markdown=True
        )

        enhanced_prompt = f"""
        Create a cohesive playlist based on this request: "{user_prompt}"
        Consider:
        - Musical progression
        - Mood transitions
        - Artist variety
        - Genre authenticity
        """
        response = agent.run(enhanced_prompt)
        json_text = extract_json(response.content)
        try:
            recommendations = json.loads(json_text)
            if not recommendations:
                logger.warning("No recommendations extracted, consider refining the prompt.")
            else:
                logger.info(f"Generated {len(recommendations)} song recommendations")
            return recommendations
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}\nResponse Content: {json_text}")
            return []
    except Exception as e:
        logger.error(f"Error in prompt processing: {e}")
        return []
