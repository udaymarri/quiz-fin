from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import firebase_admin
import os
from firebase_admin import credentials, firestore, auth
import json
from typing import List, Optional, Dict
from datetime import datetime
import httpx
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
IS_GENERIC_KEY = GEMINI_API_KEY is None or GEMINI_API_KEY == ""

if GEMINI_API_KEY:
        logger.info(f"Initializing Gemini AI (REST) with [gemini-pro]")
else:
        logger.warning("GEMINI_API_KEY not found. AI features will be in mock mode.")

app = FastAPI(title="QuizMaster Pro API")

# Enable CORS
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
)

# Enable CORS
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
)

# Initialize Firebase Admin
def init_firebase():
        if firebase_admin._apps:
                    return firestore.client()
                service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    if service_account_json:
                try:
                                logger.info("Initializing Firebase with FIREBASE_SERVICE_ACCOUNT_JSON")
                                cred_dict = json.loads(service_account_json)
                                cred = credentials.Certificate(cred_dict)
                                firebase_admin.initialize_app(cred)
                                return firestore.client()
except Exception as e:
            logger.error(f"Failed to initialize Firebase from JSON env var: {e}")
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if cred_path and os.path.exists(cred_path):
                try:
                                logger.info(f"Initializing Firebase from {cred_path}")
                                cred = credentials.Certificate(cred_path)
                                firebase_admin.initialize_app(cred)
                                return firestore.client()
except Exception as e:
            logger.error(f"Failed to initialize Firebase from file: {e}")
    try:
                logger.info("Initializing Firebase with default credentials")
                firebase_admin.initialize_app()
                return firestore.client()
except Exception as e:
        logger.error(f"Default Firebase initialization failed: {e}")
    return None

db = init_firebase()
if db:
        logger.info("Firebase Firestore initialized successfully")
else:
    logger.warning("Falling back to mock data store")

mock_questions_store = [
        {"id": "mock-1", "question": "What is the capital of France?", "options": ["London", "Berlin", "Paris", "Madrid"], "correctAnswer": 2, "category": "geography", "difficulty": "easy"},
        {"id": "mock-2", "question": "Which planet is known as the Red Planet?", "options": ["Venus", "Jupiter", "Mars", "Saturn"], "correctAnswer": 2, "category": "science", "difficulty": "medium"},
        {"id": "mock-3", "question": "In what year did the Titanic sink?", "options": ["1912", "1905", "1898", "1923"], "correctAnswer": 0, "category": "history", "difficulty": "hard"},
        {"id": "mock-4", "question": "What does HTTP stand for?", "options": ["HyperText Transfer Protocol", "HyperText Transmission Protocol", "Hyper Transfer Text Protocol", "HyperLink Transfer Protocol"], "correctAnswer": 0, "category": "programming", "difficulty": "easy"},
        {"id": "mock-5", "question": "Which programming language is known as the 'mother of all languages'?", "options": ["Java", "C", "Python", "Assembly"], "correctAnswer": 1, "category": "programming", "difficulty": "medium"},
        {"id": "mock-6", "question": "What is the square root of 144?", "options": ["10", "12", "14", "16"], "correctAnswer": 1, "category": "math", "difficulty": "easy"},
        {"id": "mock-7", "question": "Who painted the Mona Lisa?", "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet"], "correctAnswer": 2, "category": "general", "difficulty": "medium"},
        {"id": "mock-8", "question": "What is the largest ocean on Earth?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "correctAnswer": 3, "category": "geography", "difficulty": "easy"},
        {"id": "mock-9", "question": "Who wrote 'Hamlet'?", "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "Jane Austen"], "correctAnswer": 1, "category": "history", "difficulty": "medium"},
        {"id": "mock-10", "question": "What is the chemical symbol for Gold?", "options": ["Au", "Ag", "Pb", "Fe"], "correctAnswer": 0, "category": "science", "difficulty": "easy"}
]
mock_results_store = []

class Question(BaseModel):
        id: Optional[str] = None
    question: str
    options: List[str]
    correctAnswer: int
    category: str
    difficulty: str

class QuizResult(BaseModel):
        userId: str
    username: str
    score: int
    correctAnswers: int
    totalQuestions: int
    timeTaken: int
    category: str
    difficulty: str

class AIQuizRequest(BaseModel):
        topic: str
    difficulty: str

class ChatbotRequest(BaseModel):
        message: str

@app.get("/")
async def root():
        return {
            "message": "QuizMaster Pro API is running",
            "firebase_active": db is not None,
            "ai_active": GEMINI_API_KEY is not None and not IS_GENERIC_KEY
}

@app.get("/status")
async def status():
        return {
            "status": "healthy",
            "db": "connected" if db else "offline (mock mode)",
            "gemini_active": not IS_GENERIC_KEY,
            "firebase_active": db is not None,
            "timestamp": datetime.now().isoformat()
}

@app.get("/questions")
async def get_questions(category: Optional[str] = None, difficulty: Optional[str] = None):
        if not db:
                    res = mock_questions_store
                    if category: res = [q for q in res if q["category"] == category]
                                if difficulty: res = [q for q in res if q["difficulty"] == difficulty]
                                            return res
    questions_ref = db.collection("questions")
    query = questions_ref
    if category: query = query.where("category", "==", category)
            if difficulty: query = query.where("difficulty", "==", difficulty)
                    docs = query.stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

@app.post("/questions")
async def add_question(question: Question):
        data = question.dict(exclude_unset=True)
    if "id" in data: del data["id"]
            if not db:
                        data["id"] = f"mock-q-{len(mock_questions_store) + 100}"
        mock_questions_store.append(data)
                    return {"id": data["id"], "status": "success"}
    update_time, doc_ref = db.collection("questions").add(data)
    return {"id": doc_ref.id, "status": "success"}

@app.put("/questions/{question_id}")
async def update_question(question_id: str, question: Question):
    data = question.dict(exclude_unset=True)
    if "id" in data: del data["id"]
    if not db:
                for i, q in enumerate(mock_questions_store):
                                if q["id"] == question_id:
                                                    data["id"] = question_id
                                                    mock_questions_store[i] = data
                                                    break
                                            return {"id": question_id, "status": "success"}
    db.collection("questions").document(question_id).update(data)
    return {"id": question_id, "status": "success"}

@app.delete("/questions/{question_id}")
async def delete_question(question_id: str):
        if not db:
                    global mock_questions_store
        mock_questions_store = [q for q in mock_questions_store if q["id"] != question_id]
        return {"status": "success"}
    db.collection("questions").document(question_id).delete()
    return {"status": "success"}

@app.get("/leaderboard")
async def get_leaderboard(limit: int = 10):
        if not db:
                    base_mocks = [
                                    {"id": "user-1", "username": "QuizMaster", "score": 9500, "category": "General"},
                                    {"id": "user-2", "username": "Brainiac", "score": 8200, "category": "Science"},
            {"id": "user-3", "username": "TriviaKing", "score": 7500, "category": "History"}
                    ]
        all_results = sorted(mock_results_store + base_mocks, key=lambda x: x["score"], reverse=True)
        return all_results[:limit]
                        results_ref = db.collection("results")
    docs = results_ref.order_by("score", direction=firestore.Query.DESCENDING).limit(limit).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

@app.post("/results")
async def save_result(result: QuizResult):
    data = result.dict()
    if not db:
                data["id"] = f"mock-res-{len(mock_results_store)}"
        mock_results_store.append(data)
        return {"id": data["id"], "status": "success"}
    data["timestamp"] = firestore.SERVER_TIMESTAMP
    update_time, doc_ref = db.collection("results").add(data)
    return {"id": doc_ref.
            # Multiplayer WebSocket Logic
from collections import defaultdict
import asyncio

class ConnectionManager:
        def __init__(self):
                    self.active_connections = defaultdict(list)
        self.room_states = defaultdict(dict)
    async def connect(self, room_id, websocket):
        await websocket.accept()
                                self.active_connections[room_id].append(websocket)
                    if room_id in self.room_states:
                                    await websocket.send_json({"type": "state_update", "players": self.room_states[room_id]})
    def disconnect(self, room_id, websocket, username=None):
        if room_id in self.active_connections and websocket in self.active_connections[room_id]:
                        self.active_connections[room_id].remove(websocket)
        if username and room_id in self.room_states and username in self.room_states[room_id]:
                        del self.room_states[room_id][username]
            asyncio.create_task(self.broadcast(room_id, {"type": "state_update", "players": self.room_states[room_id]}))
    async def broadcast(self, room_id, message):
            if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                try: await connection.send_json(message)
                                    except: pass

manager = ConnectionManager()

@app.websocket("/ws/multiplayer/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
        await manager.connect(room_id, websocket)
                    current_username = None
    try:
                while True:
                                data = await websocket.receive_text()
            try:
                                msg = json.loads(data)
                action = msg.get("action")
                if action == "join":
                                        username = msg.get("username", "Anonymous")
                                        current_username = username
                                        if room_id not in manager.room_states: manager.room_states[room_id] = {}
                                                                manager.room_states[room_id][username] = {"score": 0, "isReady": False, "hasFinished": False}
                    await manager.broadcast(room_id, {"type": "state_update", "players": manager.room_states[room_id]})
elif action == "ready":
                    if current_username and current_username  in manager.room_states[room_id]:
                                                manager.room_states[room_id][current_username]["isReady"] = True
                        await manager.broadcast(room_id, {"type": "state_update", "players": manager.room_states[room_id]})
elif action == "start":
                    await manager.broadcast(room_id, {"type": "game_started"})
elif action == "update_score":
                    if current_username and current_username in manager.room_states[room_id]:
                                                manager.room_states[room_id][current_username]["score"] = msg.get("score", 0)
                                await manager.broadcast(room_id, {"type": "state_update", "players": manager.room_states[room_id]})
        elif action == "finish":
                    if current_username and current_username in manager.room_states[room_id]:
                            manager.room_states[room_id][current_username]["hasFinished"] = True
                                    await manager.broadcast(room_id, {"type": "state_update", "players": manager.room_states[room_id]})
except json.JSONDecodeError: pass
except WebSocketDisconnect:
        manager.disconnect(room_id, websocket, current_username)

            # AI Integration Logic
FALLBACK_FAQ = {
    "hi": "Hello there! I'm the QuizMaster AI Assistant. Ask me anything about the game!",
    "default": "I'm currently using my backup system. You can ask me about game rules or modes!"
}
FALLBACK_QUIZ = [{"question": "What is the capital of France?", "options": ["London", "Berlin", "Paris", "Madrid"], "correctAnswer": 2, "category": "Fallback", "difficulty": "easy"}]

async def call_gemini_rest(prompt: str):
        if not GEMINI_API_KEY: raise Exception("GEMINI_API_KEY not found")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()

        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']

@app.post("/api/generate_quiz")
async def generate_quiz(req: AIQuizRequest):
    prompt = f'Generate exactly 5 multiple-choice questions about "{req.topic}" at {req.difficulty} difficulty. Return ONLY a JSON array of objects with "question", "options" (4 strings), and "correctAnswer" (0-3).'
                            try:
                    text = await call_gemini_rest(prompt)
        text = text.replace("```json\n", "").replace("```", "").strip()
                                             questions = json.loads(text)
        for q in questions: q["category"], q["difficulty"] = "AI Generated", req.difficulty
        return questions
except Exception as e:
        logger.error(f"AI Quiz Error: {e}")
        return FALLBACK_QUIZ

@app.post("/api/chatbot")
async def chat_with_bot(req: ChatbotRequest):
    prompt = f"You are the 'QuizMaster Pro AI Assistant'. Concisely answer: {req.message}"
    try:
        response_text = await call_gemini_rest(prompt)
        return {"response": response_text}
except Exception as e:
        logger.error(f"AI Chatbot Error: {e}")
                    return {"response": FALLBACK_FAQ.get(req.message.lower(), FALLBACK_FAQ["default"])}
                                                               
