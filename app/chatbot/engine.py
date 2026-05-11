from typing import Dict, List, Optional
import uuid

QUESTIONS = [
    {"id": "name", "text": "What is your full name?", "field": "contact.name"},
    {"id": "email", "text": "What is your email address?", "field": "contact.email"},
    {"id": "phone", "text": "What is your phone number?", "field": "contact.phone"},
    {"id": "linkedin", "text": "What is your LinkedIn URL? (Optional)", "field": "contact.linkedin", "optional": True},
    {"id": "github", "text": "What is your GitHub URL? (Optional)", "field": "contact.github", "optional": True},
    {"id": "role", "text": "What is your target job role? (e.g. Full Stack Developer)", "field": "role"},
    {"id": "skills", "text": "List your top skills (comma separated)", "field": "skills"},
    {"id": "experience", "text": "Tell me about your latest work experience. (Format: Job Title, Company, Dates, Description)", "field": "experience"},
    {"id": "education", "text": "Enter your education details. (Format: Degree, Institution, Year)", "field": "education"},
    {"id": "projects", "text": "Describe a major project you've worked on. (Format: Title, Description, Technologies)", "field": "projects"},
]

class ChatbotEngine:
    def __init__(self):
        self.sessions: Dict[str, dict] = {}

    def start_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "current_index": 0,
            "answers": {},
            "is_completed": False
        }
        return session_id

    def get_question(self, session_id: str) -> Optional[dict]:
        session = self.sessions.get(session_id)
        if not session or session["is_completed"]:
            return None
        
        index = session["current_index"]
        if index < len(QUESTIONS):
            return QUESTIONS[index]
        return None

    def submit_answer(self, session_id: str, answer: str) -> dict:
        session = self.sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}
        
        index = session["current_index"]
        question = QUESTIONS[index]
        
        # Store answer
        session["answers"][question["id"]] = answer
        
        # Move to next
        session["current_index"] += 1
        if session["current_index"] >= len(QUESTIONS):
            session["is_completed"] = True
            
        return {
            "next_question": self.get_question(session_id),
            "is_completed": session["is_completed"]
        }

    def get_session_data(self, session_id: str) -> Optional[dict]:
        return self.sessions.get(session_id)

chatbot_engine = ChatbotEngine()
