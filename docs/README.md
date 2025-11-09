# JEE Physics AI Tutor

An AI-powered Socratic tutor for JEE Physics that guides students through problem-solving using questions and hints instead of just providing answers.

## Features

- **User Input Mode**: Paste ANY physics question - the AI will guide you through it
- **Flexible Question Types**: Support for MCQ, Numerical, and Descriptive questions
- **Interactive Chat Interface**: Engage with AI tutor in real-time using Socratic method
- **3-Level Hint System**: Get progressive hints when stuck
- **Sample Problems**: Access curated JEE problems from the database (optional)
- **Complete Solutions**: Step-by-step explanations (for curated problems)

## Setup Instructions

### 1. Install Dependencies

```bash
# Activate virtual environment (if not already activated)
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Mac/Linux

# Install required packages
pip install -r requirements.txt
```

### 2. Set Up AI (Google Gemini API)

**Get your FREE API key:**
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in and create an API key
3. Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_api_key_here
```

**See detailed instructions:** [SETUP_AI.md](SETUP_AI.md)

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Project Structure

```
NCERT/
├── app.py                    # Main Streamlit application
├── utils.py                  # Problem loader and utilities
├── requirements.txt          # Python dependencies
├── Userstory.md             # Project documentation
├── template.json            # Problem structure template
├── Topic_prblm/             # JEE problems by topic
│   ├── laws_of_motion_questions.json
│   ├── center_of_mass_questions.json
│   ├── rotation_questions.json
│   └── work_power_energy_questions.json
└── Textbooks/               # NCERT PDF textbooks
    ├── Laws-of-Motion.pdf
    ├── Motion-In-a-Plane.pdf
    ├── System-of-particles-Rotational-motion.pdf
    └── wokr-power-energy.pdf
```

## How to Use

### Method 1: Enter Your Own Question (Primary Mode)
1. **Paste your question**: Copy any JEE Physics problem into the text area
2. **Select question type**: MCQ, Numerical, or Descriptive
3. **Add options** (if MCQ): Enter the 4 options
4. **Click "Start Learning"**: Begin chatting with AI tutor
5. **Get guided**: AI asks Socratic questions to help you discover the solution
6. **Request hints**: Use hint button when truly stuck

### Method 2: Try Sample Problems (Optional)
1. **Browse samples**: Check "Browse Sample Problems" in sidebar
2. **Load an example**: Click on any topic to load a curated problem
3. **Same flow**: Follow steps 4-6 above

## Current Status

✅ UI with user question input form
✅ Support for MCQ, Numerical, and Descriptive questions
✅ Full AI integration with Google Gemini
✅ Socratic dialogue system (asks guiding questions)
✅ 3-level intelligent hint system
✅ AI-generated solutions for user questions
✅ Sample problem browser (optional)
⏳ NCERT knowledge base (RAG) - optional enhancement
⏳ Image/diagram support

## Next Steps (Optional Enhancements)

1. Build RAG system for NCERT content (more contextual responses)
2. Add support for image-based questions (diagrams, graphs)
3. Implement answer validation (check if student's answer is correct)
4. Add progress tracking and analytics
5. Multi-language support (Hindi, regional languages)
