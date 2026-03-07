# api/auth.py

import os
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

# ---------- LOAD ENV ----------
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_secret_key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 30))

# ---------- PASSWORD HASHING ----------
# 🔥 bcrypt हटाया → sha256 (Windows + Py3.13 safe)
pwd_context = CryptContext(
    schemes=["sha256_crypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ---------- DEMO USER ----------
# (Production में DB होता है)
fake_user = {
    "username": "admin",
    "hashed_password": pwd_context.hash("admin123")
}

# ---------- UTILS ----------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str) -> Optional[dict]:
    if username != fake_user["username"]:
        return None
    if not verify_password(password, fake_user["hashed_password"]):
        return None
    return {"username": username}

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception