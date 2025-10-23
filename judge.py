"""
LLM-as-a-Judge evaluation logic using Gemini API
"""
import re
import google.generativeai as genai
from typing import Tuple, Optional, Dict


EVALUATION_PROMPT = """You are an expert evaluator assessing the quality of AI-generated answers.

**Context/Question:**
---
{question}
---

**Answer:**
---
{answer}
---

Please evaluate the answer based on the following criteria on a scale of 1 to 10:

1.  **Relevance**: How relevant is the response to the given input and context?
    - 1: Completely irrelevant.
    - 5: Partially relevant, but misses key aspects of the question.
    - 10: Perfectly relevant and directly addresses all parts of the question.

2.  **Clarity**: How clear and understandable is the generated output?
    - 1: Incoherent and impossible to understand.
    - 5: Understandable, but requires effort to follow due to poor structure or jargon.
    - 10: Perfectly clear, concise, and easy to understand.
    
3.  **Consistency**: How consistent are the results across multiple runs?
    - 1: Highly inconsistent and contradictory.
    - 5: Generally consistent, but with some contradictions.
    - 10: Perfectly consistent and reliable.
    
4.  **Creativity/Innovation**: For creative tasks, how original or innovative is the output?
    - 1: Plagiarized or completely unoriginal.
    - 5: Some originality, but mostly derivative.
    - 10: Highly original and innovative.

Provide your evaluation in the following format:

**Relevance:** [Your detailed feedback on relevance]
**Relevance Score:** [A number from 1 to 10]

**Clarity:** [Your detailed feedback on clarity]
**Clarity Score:** [A number from 1 to 10]

**Consistency:** [Your detailed feedback on consistency]
**Consistency Score:** [A number from 1 to 10]

**Creativity/Innovation:** [Your detailed feedback on creativity]
**Creativity Score:** [A number from 1 to 10]

**Total Score:** [The average of all scores, from 1 to 10]
"""


def configure_gemini(api_key: str) -> None:
    """Configure the Gemini API with the provided API key."""
    genai.configure(api_key=api_key)


def evaluate_with_gemini(
    question: str,
    answer: str,
    model_name: str = "gemini-2.5-flash",
    temperature: float = 0.5
) -> Tuple[str, Dict[str, Optional[int]], str]:
    """
    Evaluate an answer using Gemini API.
    
    Args:
        question: The original question
        answer: The model-generated answer to evaluate
        model_name: The Gemini model to use for evaluation
        temperature: The temperature for the model generation
    
    Returns:
        Tuple of (feedback_text, scores_dict, prompt_text)
    """
    try:
        # Create the prompt
        prompt = EVALUATION_PROMPT.format(question=question, answer=answer)
        
        # Initialize the model
        generation_config = {"temperature": temperature}
        model = genai.GenerativeModel(
            model_name,
            generation_config=generation_config
        )
        
        # Generate evaluation
        response = model.generate_content(prompt)
        
        # Extract the response text
        feedback_text = response.text
        
        # Parse the rating from the response
        scores = {
            "total": extract_rating(feedback_text),
            "relevance": extract_relevance_score(feedback_text),
            "clarity": extract_clarity_score(feedback_text),
            "consistency": extract_consistency_score(feedback_text),
            "creativity": extract_creativity_score(feedback_text),
        }
            
        return feedback_text, scores, prompt
        
    except Exception as e:
        error_msg = f"Error during evaluation: {str(e)}"
        prompt_for_error = EVALUATION_PROMPT.format(question=question, answer=answer)
        return error_msg, {
            "total": None, "relevance": None, "clarity": None,
            "consistency": None, "creativity": None
        }, prompt_for_error


def extract_rating(text: str) -> Optional[int]:
    """
    Extract the rating from the evaluation text.
    
    Args:
        text: The evaluation response text
    
    Returns:
        The rating as an integer or None if not found
    """
    # Look for patterns like "Total Rating: 3" or "Rating:** 3" or "Total Score: 8"
    patterns = [
        r'Total Score[:\s]*\*?\*?\s*(\d{1,2})',
        r'Total Rating[:\s]*\*?\*?\s*(\d{1,2})',
        r'Rating[:\s]*\*?\*?\s*(\d{1,2})',
        r'Score[:\s]*\*?\*?\s*(\d{1,2})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            rating = int(match.group(1))
            if 1 <= rating <= 10:
                return rating
    
    return None


def extract_relevance_score(text: str) -> Optional[int]:
    """
    Extract the relevance score (1-10) from the evaluation text.
    
    Args:
        text: The evaluation response text
    
    Returns:
        The relevance score as an integer (1-10) or None if not found
    """
    match = re.search(r'Relevance Score[:\s-]*\*?\*?\s*(\d{1,2})', text, re.IGNORECASE)
    if match:
        score = int(match.group(1))
        if 1 <= score <= 10:
            return score
    return None


def extract_clarity_score(text: str) -> Optional[int]:
    """
    Extract the clarity score (1-10) from the evaluation text.
    
    Args:
        text: The evaluation response text
    
    Returns:
        The clarity score as an integer (1-10) or None if not found
    """
    match = re.search(r'Clarity Score[:\s-]*\*?\*?\s*(\d{1,2})', text, re.IGNORECASE)
    if match:
        score = int(match.group(1))
        if 1 <= score <= 10:
            return score
    return None


def extract_consistency_score(text: str) -> Optional[int]:
    """
    Extract the consistency score (1-10) from the evaluation text.
    """
    match = re.search(r'Consistency Score[:\s-]*\*?\*?\s*(\d{1,2})', text, re.IGNORECASE)
    if match:
        score = int(match.group(1))
        if 1 <= score <= 10:
            return score
    return None


def extract_creativity_score(text: str) -> Optional[int]:
    """
    Extract the creativity score (1-10) from the evaluation text.
    """
    match = re.search(r'Creativity(?:/Innovation)? Score[:\s-]*\*?\*?\s*(\d{1,2})', text, re.IGNORECASE)
    if match:
        score = int(match.group(1))
        if 1 <= score <= 10:
            return score
    return None


def generate_with_llm(
    prompt: str,
    provider: str,
    model_name: str,
    temperature: float = 0.5
) -> str:
    """
    Generate content using a specified LLM provider.
    
    Args:
        prompt: The full prompt to send to the model
        provider: The LLM provider ('gemini' or 'openai')
        model_name: The specific model to use
        temperature: The generation temperature
        
    Returns:
        The generated text content
    """
    try:
        if provider == 'gemini':
            generation_config = {"temperature": temperature}
            model = genai.GenerativeModel(
                model_name,
                generation_config=generation_config
            )
            response = model.generate_content(prompt)
            return response.text
        else:
            return f"Error: Unsupported provider '{provider}'"
            
    except Exception as e:
        return f"Error during generation: {str(e)}"