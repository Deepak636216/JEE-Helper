from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
import time
import json
from datetime import datetime
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_tutor import PhysicsAITutor
from app.services.utils import ProblemLoader

# Configure logging
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'api_requests.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="JEE Physics AI Tutor API",
    description="Socratic AI tutor for JEE Physics problems",
    version="1.0.0"
)

# CORS middleware - Allow localhost + production frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://jee-helper-one.vercel.app",  # Production Vercel deployment
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI tutor and problem loader
try:
    ai_tutor = PhysicsAITutor()
    problem_loader = ProblemLoader()
    logger.info("AI Tutor and Problem Loader initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize: {e}")
    ai_tutor = None
    problem_loader = None

# Pydantic models
class QuestionSubmission(BaseModel):
    text: str
    type: str  # "objective_single_correct", "numerical", "descriptive"
    topic: Optional[str] = "General Physics"
    difficulty: Optional[str] = "medium"
    options: Optional[List[Dict[str, str]]] = None

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    problem: Dict
    conversation_history: List[Dict]
    user_message: str

class HintRequest(BaseModel):
    problem: Dict
    conversation_history: List[Dict]
    hint_level: int

class SolutionRequest(BaseModel):
    problem: Dict

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = f"{int(time.time() * 1000)}"
    start_time = time.time()

    # Log request
    logger.info(f"REQUEST [{request_id}] {request.method} {request.url.path}")

    try:
        # Get request body for POST requests
        if request.method == "POST":
            body = await request.body()
            if body:
                try:
                    body_json = json.loads(body)
                    logger.info(f"REQUEST BODY [{request_id}]: {json.dumps(body_json, indent=2)}")
                except:
                    pass
                # Re-create request with body
                from starlette.requests import Request as StarletteRequest
                async def receive():
                    return {"type": "http.request", "body": body}
                request = StarletteRequest(request.scope, receive)

        response = await call_next(request)

        # Log response
        duration = time.time() - start_time
        logger.info(f"RESPONSE [{request_id}] Status: {response.status_code} Duration: {duration:.2f}s")

        return response

    except Exception as e:
        logger.error(f"ERROR [{request_id}]: {str(e)}", exc_info=True)
        raise

# Health check
@app.get("/")
async def root():
    return {
        "message": "JEE Physics AI Tutor API",
        "status": "running",
        "ai_enabled": ai_tutor is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_tutor": ai_tutor is not None,
        "problem_loader": problem_loader is not None,
        "timestamp": datetime.now().isoformat()
    }

# Endpoints for topics/chapters/samples removed - not needed for simplified UI
# Students just paste their questions directly

# Submit a new question
@app.post("/api/question/submit")
async def submit_question(question: QuestionSubmission):
    try:
        logger.info(f"Question submitted: {question.text[:100]}...")

        problem = {
            "text": question.text,
            "type": question.type,
            "topic": question.topic,
            "difficulty": question.difficulty,
            "user_submitted": True
        }

        if question.options:
            problem["options"] = question.options

        # Get initial AI message
        if not ai_tutor:
            raise HTTPException(status_code=503, detail="AI Tutor not available. Check API key.")

        initial_message = ai_tutor.get_initial_message(problem)

        logger.info(f"Initial message generated: {initial_message[:100]}...")

        return {
            "problem": problem,
            "initial_message": initial_message,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error submitting question: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Chat with AI tutor
@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        logger.info(f"Chat request - User message: {request.user_message[:100]}...")

        if not ai_tutor:
            raise HTTPException(status_code=503, detail="AI Tutor not available. Check API key.")

        response = ai_tutor.get_response(
            problem=request.problem,
            conversation_history=request.conversation_history,
            user_message=request.user_message
        )

        logger.info(f"AI response: {response[:100]}...")

        return {
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Get hint
@app.post("/api/hint")
async def get_hint(request: HintRequest):
    try:
        logger.info(f"Hint requested - Level: {request.hint_level}")

        if not ai_tutor:
            raise HTTPException(status_code=503, detail="AI Tutor not available. Check API key.")

        hint = ai_tutor.get_hint(
            problem=request.problem,
            conversation_history=request.conversation_history,
            hint_level=request.hint_level
        )

        logger.info(f"Hint generated: {hint[:100]}...")

        return {
            "hint": hint,
            "level": request.hint_level,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating hint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Get solution
@app.post("/api/solution")
async def get_solution(request: SolutionRequest):
    try:
        logger.info(f"Solution requested for problem")

        # Check if it's a curated problem with official solution
        if 'official_solution' in request.problem and not request.problem.get('user_submitted', False):
            logger.info("Returning official solution")
            return {
                "solution": request.problem['official_solution'],
                "type": "official",
                "timestamp": datetime.now().isoformat()
            }

        # Generate solution using AI
        if not ai_tutor:
            raise HTTPException(status_code=503, detail="AI Tutor not available. Check API key.")

        solution = ai_tutor.generate_solution(request.problem)

        logger.info(f"AI solution generated")

        return {
            "solution": solution,
            "type": "ai_generated",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating solution: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
