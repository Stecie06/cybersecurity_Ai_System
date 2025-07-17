from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import firebase_admin
from firebase_admin import auth, credentials
import os
from pathlib import Path
from typing import Optional

# Initialize FastAPI
app = FastAPI(title="Threat Intelligence API")

# Setup CORS (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only!
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Firebase Admin Setup
current_dir = Path(__file__).parent
cred_path = current_dir / "firebase_credentials" / "serviceAccountKey.json"

if not cred_path.exists():
    raise FileNotFoundError(f"Firebase key not found at {cred_path}")

cred = credentials.Certificate(str(cred_path))
firebase_admin.initialize_app(cred)

# Security
security = HTTPBearer()

# Data Models
class UserLogin(BaseModel):
    email: str
    password: str

class UserToken(BaseModel):
    token: str
    uid: str
    email: str

# Helper Functions
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Auth Endpoints
@app.post("/login", response_model=UserToken)
async def login(user_data: UserLogin):
    """Authenticate users and return Firebase token"""
    try:
        # Verify user exists
        user = auth.get_user_by_email(user_data.email)
        
        # In production, you would verify password here
        # This is just for demonstration - use Firebase Auth client-side
        custom_token = auth.create_custom_token(user.uid)
        
        return {
            "token": custom_token.decode(),
            "uid": user.uid,
            "email": user.email
        }
    except auth.UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

# Protected Endpoints
@app.get("/threat-reports")
async def get_threats(user: dict = Depends(get_current_user)):
    """Get all threats (requires authentication)"""
    import pandas as pd
    try:
        df = pd.read_csv("logs/central_reports.csv")
        return df.to_dict('records')
    except FileNotFoundError:
        return []

@app.get("/alerts")
async def get_alerts(user: dict = Depends(get_current_user)):
    """Get critical alerts (requires authentication)"""
    import pandas as pd
    try:
        df = pd.read_csv("logs/central_reports.csv")
        return df[df['threat_level'] == 'CRITICAL'].to_dict('records')
    except FileNotFoundError:
        return []

# Health Check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}