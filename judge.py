"""
LLM-as-a-Judge evaluation logic using Gemini API
"""
import re
import google.generativeai as genai
from typing import Tuple, Optional


IMPROVED_JUDGE_PROMPT = """You are an expert evaluator assessing the quality of AI-generated answers.

Question: {question}

Answer: {answer}

Please evaluate this answer based on the following criteria:
1. **Accuracy**: Is the answer factually correct and relevant to the question?
2. **Completeness**: Does it address all aspects of the question?
3. **Clarity**: Is the answer well-structured and easy to understand?
4. **Depth**: Does it provide sufficient detail and insight?

Provide your evaluation in the following format:

**Evaluation:**
[Your detailed feedback here]

**Total Rating:** [A number from 1 to 4, where:
- 1 = Poor (major issues in accuracy, completeness, or clarity)
- 2 = Fair (some issues but partially addresses the question)
- 3 = Good (solid answer with minor issues)
- 4 = Excellent (comprehensive, accurate, and well-presented)]
"""


def configure_gemini(api_key: str) -> None:
    """Configure the Gemini API with the provided API key."""
    genai.configure(api_key=api_key)


def evaluate_with_gemini(
    question: str,
    answer: str,
    model_name: str = "gemini-2.5-flash"
) -> Tuple[str, Optional[int]]:
    """
    Evaluate an answer using Gemini API.
    
    Args:
        question: The original question
        answer: The model-generated answer to evaluate
        model_name: The Gemini model to use for evaluation
    
    Returns:
        Tuple of (feedback_text, rating) where rating is 1-4 or None if parsing failed
    """
    try:
        # Create the prompt
        prompt = IMPROVED_JUDGE_PROMPT.format(question=question, answer=answer)
        
        # Initialize the model
        model = genai.GenerativeModel(model_name)
        
        # Generate evaluation
        response = model.generate_content(prompt)
        
        # Extract the response text
        feedback_text = response.text
        
        # Parse the rating from the response
        rating = extract_rating(feedback_text)
        
        return feedback_text, rating
        
    except Exception as e:
        error_msg = f"Error during evaluation: {str(e)}"
        return error_msg, None


def extract_rating(text: str) -> Optional[int]:
    """
    Extract the rating (1-4) from the evaluation text.
    
    Args:
        text: The evaluation response text
    
    Returns:
        The rating as an integer (1-4) or None if not found
    """
    # Look for patterns like "Total Rating: 3" or "Rating:** 3"
    patterns = [
        r'Total Rating[:\s]*\*?\*?\s*(\d)',
        r'Rating[:\s]*\*?\*?\s*(\d)',
        r'Score[:\s]*\*?\*?\s*(\d)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            rating = int(match.group(1))
            if 1 <= rating <= 4:
                return rating
    
    return None

