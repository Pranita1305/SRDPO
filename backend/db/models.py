from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[str]
    name: str
    email: EmailStr
    password_hash: str
    role: str = "user"

class RidePrediction(BaseModel):
    timestamp: datetime
    zone_id: int
    predicted_demand: float
    model_used: str

class ZoneCluster(BaseModel):
    zone_id: int
    cluster_id: int
    lat: float
    lon: float
    cluster_name: str

class SurgeAlert(BaseModel):
    timestamp: datetime
    zone_id: int
    predicted_demand: float
    price_factor: float
    status: str
