# 🧾 PRD: LLM Evaluation Playground (Python + Streamlit + Pydantic)

## 🎯 Goal
Create a simple **Streamlit** web app that lets users evaluate model-generated outputs using:
1. **LLM-as-a-Judge Evaluation** – via Gemini API  
2. **Pydantic Validation** – for structural completeness checking  
3. **CSV Logging** – store all inputs and outputs from each run  

The design should remain simple and focus primarily on evaluation logic and traceability.

---

## 🧱 Tech Stack

| Layer | Tool |
|--------|------|
| Frontend | Streamlit |
| Backend | Python |
| Model | Google Gemini API |
| Validation | Pydantic |
| Data Logging | CSV (`pandas`) |
| Environment | `.env` for `GOOGLE_API_KEY` |

---

## ⚙️ Features

### 1. Input Form
- **Text area for Question**
- **Text area for Model Answer**
- **Dropdown to select Gemini model** (`gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`)
- **Evaluate** button

### 2. Processing Logic
1. Combine question and answer into `IMPROVED_JUDGE_PROMPT`.
2. Send to Gemini model for evaluation.
3. Parse the returned text for:
   - **Evaluation (feedback)**
   - **Total rating (1–4)**
4. Validate the model answer against the **Pydantic schema**.
5. Log inputs + outputs + evaluation results to CSV.

### 3. Output Display
- Feedback from Gemini
- Total rating (1–4)
- Pydantic validation status (valid or error message)
- Confirmation message: “✅ Results saved to evaluations.csv”

---

## 🧩 Data Logging to CSV

| Column | Description |
|---------|--------------|
| `timestamp` | Time of evaluation |
| `model` | Selected Gemini model |
| `question` | Input prompt |
| `answer` | Model-generated output |
| `judge_feedback` | Feedback text from Gemini |
| `total_rating` | Extracted rating (1–4) |
| `validation_status` | Result of Pydantic validation |
| `completeness_score` | 1.0 (valid) or 0.0 (invalid) |

Stored in `evaluations.csv` and appended after every run.

---

## 📁 File Structure

