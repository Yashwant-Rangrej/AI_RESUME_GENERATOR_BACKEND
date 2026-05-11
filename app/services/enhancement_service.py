from typing import List

def enhance_project_description(description: str) -> str:
    """
    Enhances a simple project description into a more professional one.
    """
    desc_lower = description.lower()
    
    # Simple rule-based enhancement
    if "made website" in desc_lower or "built website" in desc_lower:
        return "Developed a responsive web-based application with a user-friendly interface and optimized performance."
    
    if "school" in desc_lower and "management" in desc_lower:
        return "Architected a comprehensive school management system streamlining administrative tasks and enhancing student data tracking."
    
    if "app" in desc_lower or "application" in desc_lower:
        return f"Engineered a robust {description} focusing on scalability, security, and seamless user experience."
    
    # Fallback: Just capitalize and add a professional prefix if it seems too short
    if len(description.split()) < 5:
        return f"Designed and implemented a {description} using modern development best practices."
    
    return description

def parse_input_string(input_str: str, fields: List[str]) -> dict:
    """
    Helper to parse comma-separated strings into a dictionary.
    """
    parts = [p.strip() for p in input_str.split(",")]
    result = {}
    for i, field in enumerate(fields):
        if i < len(parts):
            result[field] = parts[i]
        else:
            result[field] = ""
    return result
