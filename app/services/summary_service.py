from typing import List

def generate_summary(skills: List[str], role: str) -> str:
    """
    Generates a professional summary based on skills and target role.
    """
    if not skills or not role:
        return "Dedicated professional with a strong background in software development and a passion for building innovative solutions."
    
    top_skills = skills[:4]
    summary = f"Passionate {role} skilled in {', '.join(top_skills)} with strong interest in software development and problem solving. "
    summary += f"Committed to delivering high-quality code and optimizing system performance to meet business goals."
    
    return summary
