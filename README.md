# JEE Physics AI Tutor

An intelligent Socratic tutor for JEE Physics problems using Google Gemini AI.

## Project Structure

```
NCERT/
├── backend/                  # FastAPI backend server
│   ├── app/
│   │   ├── api/             # API routes (future)
│   │   ├── core/            # Core configurations (future)
│   │   ├── models/          # Pydantic models (future)
│   │   └── services/        # Business logic
│   │       ├── ai_tutor.py  # AI tutor implementation
│   │       └── utils.py     # Utility functions
│   ├── data/
│   │   ├── textbooks/       # PDF textbooks
│   │   └── problems/        # Problem JSON files
│   ├── logs/                # Application logs
│   ├── main.py             # FastAPI application entry point
│   └── requirements.txt     # Python dependencies
│
├── frontend/                # React + Vite frontend
│   ├── src/
│   │   ├── api/            # API client
│   │   ├── components/     # React components
│   │   ├── App.jsx         # Main app component
│   │   └── main.jsx        # Entry point
│   ├── index.html
│   └── package.json
│
├── config/                  # Configuration files
│   ├── .env               # Environment variables (not in git)
│   └── .env.example       # Environment template
│
├── docs/                   # Documentation
│   ├── AI_INTEGRATION_COMPLETE.md
│   ├── REACT_FASTAPI_SETUP.md
│   ├── README.md
│   ├── SETUP_AI.md
│   ├── UI_CHANGES.md
│   └── Userstory.md
│
└── scripts/               # Utility scripts
    ├── start_backend.bat  # Start backend server
    └── start_frontend.bat # Start frontend dev server

```

## Features

- Socratic method teaching approach
- Interactive problem solving
- Progressive hints system
- Support for multiple question types
- Topic-based problem filtering
- Integrated with Google Gemini AI

## Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API key

### Backend Setup

1. Install Python dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Configure environment:
   ```bash
   cd ../config
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

3. Start backend server:
   ```bash
   # From project root
   scripts/start_backend.bat
   # Or manually:
   cd backend
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start development server:
   ```bash
   # From project root
   scripts/start_frontend.bat
   # Or manually:
   cd frontend
   npm run dev
   ```

### Quick Start (Windows)

Run both servers with the scripts:
```bash
# Terminal 1 - Backend
scripts\start_backend.bat

# Terminal 2 - Frontend
scripts\start_frontend.bat
```

## API Endpoints

- `GET /` - Health check
- `GET /api/topics` - Get all topics
- `GET /api/chapters` - Get all chapters
- `GET /api/problems/samples` - Get sample problems
- `POST /api/question/submit` - Submit a new question
- `POST /api/chat` - Chat with AI tutor
- `POST /api/hint` - Get a hint
- `POST /api/solution` - Get solution

## Usage

1. Open http://localhost:5173 in your browser
2. Select a topic or submit your own question
3. Interact with the AI tutor using the Socratic method
4. Request hints when needed
5. View complete solutions after attempting the problem

## Development

### Backend
- FastAPI framework
- Google Gemini AI integration
- Structured logging
- CORS enabled for local development

### Frontend
- React 18 with Vite
- Modern component structure
- API client abstraction
- Responsive UI

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
