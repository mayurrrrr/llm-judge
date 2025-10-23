"""
CSV logging functionality
"""
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional
import os


CSV_FILE = "evaluations.csv"
CSV_HEADER = [
    "timestamp", "model", "temperature", "question", "answer", "judge_feedback",
    "judge_prompt", "total_rating(1-10)", "validation_status", "relevance_score",
    "clarity_score", "consistency_score", "creativity_score"
]


def log_evaluation(
    model: str,
    temperature: float,
    question: str,
    answer: str,
    judge_feedback: str,
    judge_prompt: str,
    total_rating: Optional[int],
    validation_status: str,
    relevance_score: Optional[int],
    clarity_score: Optional[int],
    consistency_score: Optional[int],
    creativity_score: Optional[int]
):
    """
    Log an evaluation to a CSV file.
    
    Args:
        model: Name of the model being evaluated
        temperature: The temperature used for the judge model
        question: The question asked
        answer: The answer provided by the model
        judge_feedback: Feedback from the LLM judge
        judge_prompt: The prompt sent to the LLM judge
        total_rating: Rating from the LLM judge
        validation_status: Status of Pydantic validation
        relevance_score: Relevance score from the judge
        clarity_score: Clarity score from the judge
        consistency_score: Consistency score from the judge
        creativity_score: Creativity score from the judge
    """
    now = datetime.now()
    
    # Create a dictionary for the new row
    new_row = {
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "model": model,
        "temperature": temperature,
        "question": question,
        "answer": answer,
        "judge_feedback": judge_feedback,
        "judge_prompt": judge_prompt,
        "total_rating(1-10)": total_rating,
        "validation_status": validation_status,
        "relevance_score": relevance_score,
        "clarity_score": clarity_score,
        "consistency_score": consistency_score,
        "creativity_score": creativity_score
    }
    
    # Check if file exists to write header
    csv_path = Path(CSV_FILE)
    
    if csv_path.exists() and csv_path.stat().st_size > 0:
        # Append to existing file
        df = pd.read_csv(csv_path)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        # Create new file
        df = pd.DataFrame([new_row], columns=CSV_HEADER)
    
    # Save to CSV
    df.to_csv(csv_path, index=False)


def get_evaluation_history() -> pd.DataFrame:
    """
    Load the evaluation history from CSV.
    
    Returns:
        DataFrame with evaluation history, or empty DataFrame if file doesn't exist
    """
    csv_path = Path(CSV_FILE)
    
    if csv_path.exists() and csv_path.stat().st_size > 0:
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=CSV_HEADER)

