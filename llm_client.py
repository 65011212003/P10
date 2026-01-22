"""Module for interacting with the DeepSeek LLM API."""

import json
import time
from typing import Callable, Optional

from openai import OpenAI, APIError, RateLimitError, APIConnectionError

from config import (
    DEEPSEEK_API_KEY, 
    DEEPSEEK_BASE_URL, 
    DEEPSEEK_MODEL,
    MAX_TOKENS,
    MAX_INPUT_CHARS,
    RETRY_ATTEMPTS,
    RETRY_DELAY
)


def create_client() -> OpenAI:
    """Create and return an OpenAI client configured for DeepSeek."""
    return OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )


def get_system_prompt() -> str:
    """Return the system prompt for presentation generation."""
    return """You are an expert presentation designer and content strategist. Your task is to analyze the provided content and create a comprehensive, rich PowerPoint presentation.

Return your response as a valid JSON object with the following structure:
{
    "title": "Presentation Title",
    "slides": [
        {
            "title": "Slide Title",
            "content": ["Point 1", "Point 2", "Point 3", ...],
            "notes": "Detailed speaker notes with additional context, examples, and talking points",
            "type": "content"  // Can be: "content", "section", or "comparison"
        }
    ]
}

Guidelines for RICH, COMPREHENSIVE content:
- YOU decide the optimal number of slides based on the content depth (no limit - use as many as needed)
- Extract ALL valuable information from the source - don't leave anything important out
- Each slide can have as many bullet points as needed to fully cover the topic
- Bullet points should be informative and detailed, not just keywords
- Include specific details: statistics, examples, definitions, explanations
- Add sub-points with additional context where appropriate (prefix with "  - " for nesting)
- Create dedicated slides for: Introduction, each major topic, examples, case studies, key takeaways, conclusion
- Speaker notes should be comprehensive - include background info, elaborations, and presentation tips
- If content has data/statistics, create slides specifically for those
- If content has processes/steps, break them into clear sequential slides
- If content has comparisons, create comparison slides with type "comparison"
- Ensure deep coverage - better to have more detailed slides than fewer shallow ones
- Group related concepts logically but don't over-compress information

Slide Type Guidelines:
- "content": Standard bullet point slides (default)
- "section": Use for major topic transitions/dividers (only needs title)
- "comparison": For comparing two things side by side

Content Richness Requirements:
- Explain concepts, don't just list them
- Include "why" and "how", not just "what"
- Add context and real-world applications
- Preserve technical details and specifics from the source
- Create section divider slides for major topic transitions

IMPORTANT: Return ONLY valid JSON, no markdown code blocks or additional text."""


def get_user_prompt(file_content: str, file_name: str) -> str:
    """Generate the user prompt for presentation creation."""
    # Truncate content if too long
    if len(file_content) > MAX_INPUT_CHARS:
        file_content = file_content[:MAX_INPUT_CHARS] + "\n\n[Content truncated due to length...]"
    
    return f"""Please analyze the following content from file "{file_name}" and create a COMPREHENSIVE PowerPoint presentation structure.

Extract ALL valuable information and create as many slides as needed to fully represent the content with rich detail.

---
{file_content}
---

Generate a thorough, detailed presentation that captures everything important from this content."""


def parse_llm_response(response_text: str) -> dict:
    """Parse and validate the LLM response as JSON."""
    import re
    
    # Clean up response if it contains markdown code blocks
    cleaned = response_text.strip()
    
    if "```json" in cleaned:
        cleaned = cleaned.split("```json")[1].split("```")[0]
    elif "```" in cleaned:
        # Try to extract content between first pair of ```
        parts = cleaned.split("```")
        if len(parts) >= 2:
            cleaned = parts[1]
    
    cleaned = cleaned.strip()
    
    try:
        data = json.loads(cleaned)
        
        # Validate structure
        if not isinstance(data, dict):
            raise ValueError("Response is not a JSON object")
        
        if 'slides' not in data:
            data['slides'] = []
        
        if 'title' not in data:
            data['title'] = 'Generated Presentation'
        
        return data
        
    except json.JSONDecodeError as e:
        # Try to find JSON object in the response
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        raise ValueError(f"Failed to parse LLM response as JSON: {e}\nResponse preview: {response_text[:500]}...")


def generate_presentation_content(
    file_content: str, 
    file_name: str,
    progress_callback: Optional[Callable[[float], None]] = None
) -> dict:
    """
    Use LLM to analyze file content and generate presentation structure.
    
    Args:
        file_content: The content of the file to analyze.
        file_name: The name of the source file.
        progress_callback: Optional callback for progress updates (0.0 to 1.0).
        
    Returns:
        A dictionary containing the presentation structure with slides.
    """
    client = create_client()
    
    system_prompt = get_system_prompt()
    user_prompt = get_user_prompt(file_content, file_name)
    
    last_error = None
    
    for attempt in range(RETRY_ATTEMPTS):
        try:
            # Update progress
            if progress_callback:
                progress_callback(attempt / RETRY_ATTEMPTS * 0.3)
            
            response = client.chat.completions.create(
                model=DEEPSEEK_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                stream=False,
                max_tokens=MAX_TOKENS,
                temperature=0.7,
            )
            
            # Update progress
            if progress_callback:
                progress_callback(0.8)
            
            response_text = response.choices[0].message.content
            
            # Parse and validate response
            presentation_data = parse_llm_response(response_text)
            
            # Final progress update
            if progress_callback:
                progress_callback(1.0)
            
            return presentation_data
            
        except RateLimitError as e:
            last_error = e
            wait_time = RETRY_DELAY * (attempt + 1)
            time.sleep(wait_time)
            
        except APIConnectionError as e:
            last_error = e
            if attempt < RETRY_ATTEMPTS - 1:
                time.sleep(RETRY_DELAY)
            
        except APIError as e:
            last_error = e
            if attempt < RETRY_ATTEMPTS - 1:
                time.sleep(RETRY_DELAY)
            
        except ValueError as e:
            # JSON parsing error - might get better response on retry
            last_error = e
            if attempt < RETRY_ATTEMPTS - 1:
                time.sleep(RETRY_DELAY)
    
    # All retries failed
    raise ValueError(f"Failed to generate presentation after {RETRY_ATTEMPTS} attempts. Last error: {last_error}")
