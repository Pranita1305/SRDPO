# Redis cache management

import redis
import json
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

class CacheManager:
    def __init__(self):
        self.client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    def set_prediction(self, key, data, expiry=3600):
        """Store prediction data in cache"""
        self.client.setex(key, expiry, json.dumps(data))

    def get_prediction(self, key):
        """Retrieve cached prediction if available"""
        cached_data = self.client.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None

# Example usage:
# cache = CacheManager()
# cache.set_prediction("zone_3_forecast", {"demand": 150}, 1800)
# print(cache.get_prediction("zone_3_forecast"))
