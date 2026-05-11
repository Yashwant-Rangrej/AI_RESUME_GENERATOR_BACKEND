from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.chatbot.engine import chatbot_engine
from app.services.summary_service import generate_summary
from app.services.enhancement_service import enhance_project_description, parse_input_string
from app.pdf.generator import ResumePDFGenerator
import os
import tempfile

router = APIRouter(prefix="/resume", tags=["Resume"])

@router.post("/start")
async def start_session():
    session_id = chatbot_engine.start_session()
    return {"session_id": session_id, "first_question": chatbot_engine.get_question(session_id)}

@router.get("/question")
async def get_current_question(session_id: str):
    question = chatbot_engine.get_question(session_id)
    if not question:
        raise HTTPException(status_code=404, detail="No more questions or session expired")
    return question

@router.post("/answer")
async def submit_answer(session_id: str, answer: str):
    result = chatbot_engine.submit_answer(session_id, answer)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.post("/generate")
async def generate_resume(session_id: str):
    session = chatbot_engine.get_session_data(session_id)
    if not session or not session["is_completed"]:
        raise HTTPException(status_code=400, detail="Chatbot flow not completed yet")
    
    answers = session["answers"]
    
    # Process and Enhance Data
    skills = [s.strip() for s in answers.get("skills", "").split(",")]
    role = answers.get("role", "Professional")
    summary = generate_summary(skills, role)
    
    # Parse Experience
    exp_raw = answers.get("experience", "")
    exp_parts = parse_input_string(exp_raw, ["job_title", "company", "dates", "description"])
    experience = [{
        "job_title": exp_parts["job_title"],
        "company": exp_parts["company"],
        "start_date": exp_parts["dates"].split("-")[0].strip() if "-" in exp_parts["dates"] else exp_parts["dates"],
        "end_date": exp_parts["dates"].split("-")[1].strip() if "-" in exp_parts["dates"] else "Present",
        "description": enhance_project_description(exp_parts["description"])
    }]
    
    # Parse Projects
    proj_raw = answers.get("projects", "")
    proj_parts = parse_input_string(proj_raw, ["title", "description", "technologies"])
    projects = [{
        "title": proj_parts["title"],
        "description": enhance_project_description(proj_parts["description"]),
        "technologies": [t.strip() for t in proj_parts["technologies"].split(",")]
    }]
    
    # Parse Education
    edu_raw = answers.get("education", "")
    edu_parts = parse_input_string(edu_raw, ["degree", "institution", "year"])
    education = [{
        "degree": edu_parts["degree"],
        "institution": edu_parts["institution"],
        "year": edu_parts["year"]
    }]
    
    resume_data = {
        "contact": {
            "name": answers.get("name"),
            "email": answers.get("email"),
            "phone": answers.get("phone"),
            "linkedin": answers.get("linkedin"),
            "github": answers.get("github")
        },
        "summary": summary,
        "skills": skills,
        "experience": experience,
        "projects": projects,
        "education": education
    }
    
    # Generate PDF in a temp file
    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, f"resume_{session_id}.pdf")
    
    generator = ResumePDFGenerator(pdf_path)
    generator.generate(resume_data)
    
    session["pdf_path"] = pdf_path
    
    return {"message": "Resume generated successfully", "download_url": f"/resume/download?session_id={session_id}"}

@router.get("/download")
async def download_pdf(session_id: str):
    session = chatbot_engine.get_session_data(session_id)
    if not session or "pdf_path" not in session:
        raise HTTPException(status_code=404, detail="PDF not found or not yet generated")
    
    path = session["pdf_path"]
    if not os.path.exists(path):
         raise HTTPException(status_code=404, detail="PDF file missing on server")
         
    return FileResponse(path, filename="Resume.pdf", media_type="application/pdf")
