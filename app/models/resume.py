from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import List, Optional

class ContactInfo(BaseModel):
    name: str
    email: EmailStr
    phone: str
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None

class Experience(BaseModel):
    job_title: str
    company: str
    start_date: str
    end_date: str
    description: str

class Education(BaseModel):
    degree: str
    institution: str
    year: str

class Project(BaseModel):
    title: str
    description: str
    technologies: List[str]

class ResumeData(BaseModel):
    contact: ContactInfo
    summary: Optional[str] = None
    skills: List[str]
    experience: List[Experience]
    education: List[Education]
    projects: List[Project]
    certifications: Optional[List[str]] = []

class SessionState(BaseModel):
    session_id: str
    current_question_index: int = 0
    answers: dict = {}
    is_completed: bool = False
