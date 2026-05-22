from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from app.core.config import settings

# 1. Password Locker: Ye password ko aisi secret bhasha (bcrypt) me badalta hai jise wapas normal nahi kiya ja sakta
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Normal password ko secret code (hash) me badalta hai"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check karta hai ki user ka daala hua password aur database ka secret code match karte hain ya nahi"""
    return pwd_context.verify(plain_password, hashed_password)

# 2. ID Card Generator: JWT (JSON Web Token) banata hai
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    
    # Agar time bataya hai toh theek, warna by default 30 minute baad ID card expire ho jayega
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        
    to_encode.update({"exp": expire})
    
    # Tijori (config) se secret key nikal kar ID card par sign karta hai, taaki koi nakli card na bana sake!
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encoded_jwt