from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.middleware import LogRequestMiddleware
from app.core.rate_limit import RateLimitMiddleware
from app.core.security import create_access_token, get_password_hash, verify_password

app = FastAPI(title="Agentic RAG API", version="1.0.0")

# --- GUARDS (MIDDLEWARE) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(LogRequestMiddleware)

# --- AUTHENTICATION SETUP ---
# Ye API ko batata hai ki login kahan se karna hai
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Aaj ki testing ke liye ek chhota sa nakli Database (Hardcoded password)
fake_users_db = {
    # Password ko pehle se hash (secret code) karke rakha hai
    "akshit": get_password_hash("supersecret123")
}


# --- API ENDPOINTS ---

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running!"}


# 1. RECEPTION DESK (Login karke ID Card lena)
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # User dhoondo
    if form_data.username not in fake_users_db:
        raise HTTPException(status_code=400, detail="Galat username ya password")
    
    # Password check karo
    hashed_password = fake_users_db[form_data.username]
    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(status_code=400, detail="Galat username ya password")
        
    # Agar sab sahi hai, toh ID Card (JWT Token) bana kar de do!
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


# 2. VIP ROOM (Jahan sirf valid ID Card wale ja sakte hain)
@app.get("/protected-data")
async def secret_room(token: str = Depends(oauth2_scheme)):
    # Depends(oauth2_scheme) ka matlab hai bina token ke is function ke andar aana mana hai
    return {
        "message": "Welcome to the VIP Room! 🎉", 
        "secret_data": "Ye data sirf authorized log hi dekh sakte hain.",
        "your_id_card": token
    }