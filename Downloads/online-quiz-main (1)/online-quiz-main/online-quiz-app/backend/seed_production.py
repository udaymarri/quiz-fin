import requests
import sys
import os

# Production Seeder for QuizMaster Pro
# Usage: python seed_production.py [BACKEND_URL]

DEFAULT_API_URL = "https://quiz-fin-backend.onrender.com"

# Comprehensive list of questions
QUESTIONS = [
    {"question": "What is the largest organ in the human body?", "options": ["Heart", "Brain", "Liver", "Skin"], "correctAnswer": 3, "category": "science", "difficulty": "easy"},
    {"question": "Which planet is known as the Red Planet?", "options": ["Mars", "Jupiter", "Venus", "Saturn"], "correctAnswer": 0, "category": "science", "difficulty": "easy"},
    {"question": "Who developed the theory of relativity?", "options": ["Isaac Newton", "Albert Einstein", "Nikola Tesla", "Galileo Galilei"], "correctAnswer": 1, "category": "science", "difficulty": "medium"},
    {"question": "In computing, what does CPU stand for?", "options": ["Central Processing Unit", "Computer Personal Unit", "Central Processor Unit", "Control Processing Unit"], "correctAnswer": 0, "category": "technology", "difficulty": "easy"},
    {"question": "Which programming language was created by Brendan Eich?", "options": ["Python", "JavaScript", "C++", "Ruby"], "correctAnswer": 1, "category": "technology", "difficulty": "hard"},
    {"question": "Who painted the Mona Lisa?", "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"], "correctAnswer": 2, "category": "arts", "difficulty": "easy"},
    {"question": "What is the capital of Japan?", "options": ["Seoul", "Beijing", "Tokyo", "Bangkok"], "correctAnswer": 2, "category": "geography", "difficulty": "easy"},
    {"question": "Which river is the longest in the world?", "options": ["Amazon", "Nile", "Yangtze", "Mississippi"], "correctAnswer": 1, "category": "geography", "difficulty": "medium"},
    {"question": "What is the chemical symbol for Gold?", "options": ["Ag", "Au", "Fe", "Cu"], "correctAnswer": 1, "category": "science", "difficulty": "easy"},
    {"question": "In what year did the Titanic sink?", "options": ["1905", "1912", "1918", "1923"], "correctAnswer": 1, "category": "history", "difficulty": "medium"}
]

def seed_production(api_url):
    target_url = f"{api_url.rstrip('/')}/questions"
    print(f"Targeting: {target_url}")
    success = 0
    
    for q in QUESTIONS:
        try:
            response = requests.post(target_url, json=q, timeout=10)
            if response.status_code in [200, 201]:
                success += 1
                print(f"✅ Added: {q['question']}")
            else:
                print(f"❌ Failed: {q['question']} ({response.status_code}) - {response.text}")
        except Exception as e:
            print(f"⚠️ Error: {e}")
            
    print(f"\nSeed Complete! Successfully added {success} / {len(QUESTIONS)} questions.")

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_API_URL
    seed_production(url)
