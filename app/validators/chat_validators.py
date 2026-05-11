import re
from pydantic import EmailStr, validate_email

def validate_phone(phone: str) -> bool:
    # Basic validation: 10 digits
    return phone.isdigit() and len(phone) == 10

def validate_linkedin(url: str) -> bool:
    return url.startswith("https://www.linkedin.com/") or url.startswith("https://linkedin.com/")

def validate_github(url: str) -> bool:
    return url.startswith("https://www.github.com/") or url.startswith("https://github.com/")

def validate_user_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except:
        return False
