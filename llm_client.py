"""Module for interacting with LLM APIs for presentation generation."""

import json
import re
from typing import Callable, Optional

from config import MAX_INPUT_CHARS
from llm_providers import create_provider, LLMProvider


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
    provider_name: str = "deepseek",
    progress_callback: Optional[Callable[[float], None]] = None,
    **provider_kwargs
) -> dict:
    """
    Use LLM to analyze file content and generate presentation structure.
    
    Args:
        file_content: The content of the file to analyze.
        file_name: The name of the source file.
        provider_name: LLM provider to use ('deepseek', 'openai', 'anthropic', 'ollama')
        progress_callback: Optional callback for progress updates (0.0 to 1.0).
        **provider_kwargs: Additional provider-specific arguments
        
    Returns:
        A dictionary containing the presentation structure with slides.
    """
    provider = create_provider(provider_name, **provider_kwargs)
    
    system_prompt = get_system_prompt()
    user_prompt = get_user_prompt(file_content, file_name)
    
    try:
        response_text = provider.generate(
            system_prompt,
            user_prompt,
            progress_callback
        )
        
        # Parse and validate response
        presentation_data = parse_llm_response(response_text)
        
        # Final progress update
        if progress_callback:
            progress_callback(1.0)
        
        return presentation_data
        
    except Exception as e:
        raise ValueError(f"Failed to generate presentation using {provider.get_name()}: {e}")
