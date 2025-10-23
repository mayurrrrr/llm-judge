# 🧾 LLM Evaluation Playground

A simple Streamlit web app for evaluating model-generated outputs using LLM-as-a-Judge evaluation and Pydantic validation.

## 🎯 Features

- **LLM-as-a-Judge Evaluation** – Uses Google Gemini API to evaluate answer quality
- **Pydantic Validation** – Validates structural completeness of answers
- **CSV Logging** – Automatically logs all evaluations to CSV
- **Evaluation History** – View past evaluations and metrics
- **Multiple Models** – Support for Gemini 2.5 models (Pro, Flash, Flash-Lite)

## 🚀 Setup

### 1. Clone or navigate to the project directory

```bash
cd llm-judge
```

### 2. Create a virtual environment

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Then edit `.env` and add your Google API key:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

**To get a Google API key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste it into your `.env` file

### 5. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage

1. **Enter your API key** (in the sidebar or via `.env` file)
2. **Select a Gemini model** for evaluation
3. **Enter a question** in the Question text area
4. **Enter the model's answer** in the Model Answer text area
5. **Click "Evaluate"** to run the evaluation
6. **View results**:
   - LLM judge feedback
   - Rating (1-4)
   - Pydantic validation status
   - Completeness score
7. **Check history** by toggling "Show Evaluation History"

## 🤖 Gemini 2.5 Models

The app supports three Gemini 2.5 models, each optimized for different use cases:

### **Gemini 2.5 Pro** (`gemini-2.5-pro`)
- **Best for**: Complex tasks requiring detailed analysis
- **Strengths**: 
  - Handles large datasets
  - Long context windows (over 1 million tokens)
  - Provides comprehensive, detailed responses
- **Use cases**: Long-form content, research summaries, advanced coding help

### **Gemini 2.5 Flash** (`gemini-2.5-flash`) ⚡ *Recommended*
- **Best for**: Balanced performance and quality
- **Strengths**: 
  - Optimized for speed and cost-efficiency
  - Low latency responses
  - Good quality-to-speed ratio
- **Use cases**: Real-time applications, chat, summarization, interactive experiences

### **Gemini 2.5 Flash-Lite** (`gemini-2.5-flash-lite`)
- **Best for**: High-volume, high-speed tasks
- **Strengths**: 
  - Fastest model in the 2.5 series
  - Most cost-effective option
  - High throughput
- **Use cases**: Classification, sentiment analysis, high-scale operations

## 📊 CSV Output

All evaluations are automatically saved to `evaluations.csv` with the following columns:

- `timestamp` – When the evaluation was performed
- `model` – Which Gemini model was used
- `question` – The input question
- `answer` – The model-generated answer
- `judge_feedback` – Feedback from the LLM judge
- `total_rating` – Rating from 1-4
- `validation_status` – Pydantic validation result
- `completeness_score` – 1.0 (valid) or 0.0 (invalid)

## 🏗️ Project Structure

```
llm-judge/
├── app.py              # Main Streamlit application
├── judge.py            # LLM-as-a-Judge evaluation logic
├── models.py           # Pydantic models for validation
├── logger.py           # CSV logging functionality
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment file
├── .gitignore         # Git ignore rules
├── README.md          # This file
└── PRD.md             # Product requirements document
```

## 🛠️ Customization

### Modify the Judge Prompt

Edit the `IMPROVED_JUDGE_PROMPT` in `judge.py` to customize evaluation criteria.

### Change Validation Schema

Update the `ModelAnswer` class in `models.py` to match your expected answer structure.

### Add New Models

Add more Gemini models to the dropdown in `app.py` (sidebar section).

## 📝 License

MIT License - feel free to use and modify as needed.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

