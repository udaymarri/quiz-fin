

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
