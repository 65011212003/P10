"""Module for interacting with the DeepSeek LLM API."""

from openai import OpenAI

from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL


def create_client() -> OpenAI:
    """Create and return an OpenAI client configured for DeepSeek."""
    return OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )


def generate_presentation_content(file_content: str, file_name: str) -> dict:
    """
    Use LLM to analyze file content and generate presentation structure.
    
    Args:
        file_content: The content of the file to analyze.
        file_name: The name of the source file.
        
    Returns:
        A dictionary containing the presentation structure with slides.
    """
    client = create_client()
    
    system_prompt = """You are an expert presentation designer and content strategist. Your task is to analyze the provided content and create a comprehensive, rich PowerPoint presentation.

Return your response as a valid JSON object with the following structure:
{
    "title": "Presentation Title",
    "slides": [
        {
            "title": "Slide Title",
            "content": ["Point 1", "Point 2", "Point 3", ...],
            "notes": "Detailed speaker notes with additional context, examples, and talking points"
        }
    ]
}

Guidelines for RICH, COMPREHENSIVE content:
- YOU decide the optimal number of slides based on the content depth (no limit - use as many as needed)
- Extract ALL valuable information from the source - don't leave anything important out
- Each slide can have as many bullet points as needed to fully cover the topic
- Bullet points should be informative and detailed, not just keywords
- Include specific details: statistics, examples, definitions, explanations
- Add sub-points with additional context where appropriate
- Create dedicated slides for: Introduction, each major topic, examples, case studies, key takeaways, conclusion
- Speaker notes should be comprehensive - include background info, elaborations, and presentation tips
- If content has data/statistics, create slides specifically for those
- If content has processes/steps, break them into clear sequential slides
- If content has comparisons, create comparison slides
- Ensure deep coverage - better to have more detailed slides than fewer shallow ones
- Group related concepts logically but don't over-compress information

Content Richness Requirements:
- Explain concepts, don't just list them
- Include "why" and "how", not just "what"
- Add context and real-world applications
- Preserve technical details and specifics from the source
- Create section divider slides for major topic transitions

IMPORTANT: Return ONLY valid JSON, no markdown code blocks or additional text."""

    user_prompt = f"""Please analyze the following content from file "{file_name}" and create a COMPREHENSIVE PowerPoint presentation structure.

Extract ALL valuable information and create as many slides as needed to fully represent the content with rich detail.

---
{file_content[:30000]}
---

Generate a thorough, detailed presentation that captures everything important from this content."""

    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        stream=False,
        max_tokens=8192
    )
    
    response_text = response.choices[0].message.content
    
    # Parse the JSON response
    import json
    try:
        # Clean up response if it contains markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        presentation_data = json.loads(response_text.strip())
        return presentation_data
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {e}\nResponse was: {response_text}")
