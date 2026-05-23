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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Yahan humne bataya ki keys string hain, aur values (password) bhi string hain
fake_users_db: dict[str, str] = {
    "akshit": get_password_hash("supersecret123")
}

# --- API ENDPOINTS ---

# Yahan `-> dict[str, str]` batata hai ki return me ek dictionary milegi
@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy", "message": "API is running!"}


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    if form_data.username not in fake_users_db:
        raise HTTPException(status_code=400, detail="Galat username ya password")
    
    hashed_password = fake_users_db[form_data.username]
    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(status_code=400, detail="Galat username ya password")
        
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected-data")
async def secret_room(token: str = Depends(oauth2_scheme)) -> dict[str, str]:
    return {
        "message": "Welcome to the VIP Room! 🎉", 
        "secret_data": "Ye data sirf authorized log hi dekh sakte hain.",
        "your_id_card": token
    }