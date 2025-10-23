"""
CSV logging functionality
"""
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional


CSV_FILE = "evaluations.csv"

COLUMNS = [
    "timestamp",
    "model",
    "question",
    "answer",
    "judge_feedback",
    "total_rating",
    "validation_status",
    "completeness_score"
]


def log_evaluation(
    model: str,
    question: str,
    answer: str,
    judge_feedback: str,
    total_rating: Optional[int],
    validation_status: str,
    completeness_score: float
) -> None:
    """
    Log an evaluation result to CSV file.
    
    Args:
        model: The Gemini model used
        question: The input question
        answer: The model-generated answer
        judge_feedback: Feedback from the LLM judge
        total_rating: Rating from 1-4
        validation_status: Result of Pydantic validation
        completeness_score: 1.0 if valid, 0.0 if invalid
    """
    # Create a new row
    new_row = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "question": question,
        "answer": answer,
        "judge_feedback": judge_feedback,
        "total_rating": total_rating,
        "validation_status": validation_status,
        "completeness_score": completeness_score
    }
    
    # Check if file exists
    csv_path = Path(CSV_FILE)
    
    if csv_path.exists():
        # Append to existing file
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        # Create new file
        df = pd.DataFrame([new_row])
    
    # Save to CSV
    df.to_csv(CSV_FILE, index=False)


def get_evaluation_history() -> pd.DataFrame:
    """
    Load the evaluation history from CSV.
    
    Returns:
        DataFrame with evaluation history, or empty DataFrame if file doesn't exist
    """
    csv_path = Path(CSV_FILE)
    
    if csv_path.exists():
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=COLUMNS)

