from fastapi import APIRouter, Depends
from backend.auth.dependencies import get_current_user
from backend.utils.cache_manager import redis_client
import json

router = APIRouter(prefix="/zones", tags=["Zone Clustering"])

@router.get("/heatmap")
async def get_zone_heatmap(user=Depends(get_current_user)):
    cached_data = redis_client.get("zone_heatmap")
    if cached_data:
        return json.loads(cached_data)
    return {"message": "No cached heatmap found"}
