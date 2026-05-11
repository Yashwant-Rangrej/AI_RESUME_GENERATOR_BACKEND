from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import resume_routes
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="AI Resume Builder Chatbot Backend",
    description="Rule-based resume generation system without external AI APIs.",
    version="1.0.0"
)

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(resume_routes.router)

@app.get("/")
async def root():
    return {"message": "AI Resume Builder API is running"}

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)
