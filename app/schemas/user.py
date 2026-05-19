from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

# Ye guard check karega jab naya user account banayega
class UserCreate(BaseModel):
    email: EmailStr  # Ye automatically check karega ki email format sahi hai ya nahi
    password: str
    plan: Optional[str] = "free"

    # Custom Guard: Check karo ki password strong hai ya nahi
    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password kam se kam 8 characters ka hona chahiye!")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password me kam se kam ek number (0-9) hona chahiye!")
        return v

# Ye guard check karega jab hum database se user data wapas bhejenge (Password hide karne ke liye)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    plan: str

    model_config = {"from_attributes": True} # Ye SQLAlchemy database model ko Pydantic me badal deta hai