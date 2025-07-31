# Authentication endpoints

from fastapi import APIRouter, HTTPException, Depends
from backend.db.models import User
from backend.auth.jwt_handler import hash_password, verify_password, create_access_token
from pymongo import MongoClient

router = APIRouter()
client = MongoClient("mongodb://localhost:27017")
db = client.srdapo


@router.post("/register")
def register(user: User):
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = hash_password(user.password_hash)
    db.users.insert_one({"name": user.name, "email": user.email, "password_hash": hashed_pw, "role": user.role})
    return {"msg": "User registered successfully"}


@router.post("/login")
def login(email: str, password: str):
    user = db.users.find_one({"email": email})
    if not user or not verify_password(password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"email": email, "role": user['role']})
    return {"access_token": token}
