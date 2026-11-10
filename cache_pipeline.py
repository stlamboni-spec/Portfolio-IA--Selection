# cache_pipeline.py
import time
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI(title="Cache Accelerator Engine (Redis-style)", version="1.0.0")
cache_store = {}

class CacheRequest(BaseModel):
    key: str
    value: str
    ttl_seconds: int = 60

@app.post("/api/v1/cache/set", status_code=status.HTTP_201_CREATED)
async def set_cache_value(request: CacheRequest):
    cache_store[request.key] = {
        "value": request.value,
        "expires_at": time.time() + request.ttl_seconds
    }
    return {"status": "success", "message": f"Clé '{request.key}' mise en cache."}

@app.get("/api/v1/cache/get/{key}")
async def get_cache_value(key: str):
    if key not in cache_store:
        return {"status": "miss", "value": None}
    entry = cache_store[key]
    if time.time() > entry["expires_at"]:
        del cache_store[key]
        return {"status": "expired_miss", "value": None}
    return {"status": "hit", "value": entry["value"]}
