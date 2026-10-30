from fastapi import FastAPI
from pydantic import BaseModel
import time

# Initialisation de l'API pour le Pipeline 8 (Cache Acceleration)
app = FastAPI(
    title="Pipeline 8 : Enterprise API Cache Accelerator Microservice",
    description="Microservice d'accélération d'API simulant une couche de cache (Redis layout) pour optimiser les coûts de tokens et éliminer la latence d'inférence.",
    version="1.0.0"
)

# Registre de stockage volatil en mémoire vive (RAM)
api_cache_storage = {}
CACHE_TTL_SECONDS = 300  # Time-To-Live : 5 minutes

class RequeteIA(BaseModel):
    user_prompt: str

@app.post("/cached_inference", summary="Inférence optimisée par interception de cache mémoire")
def executer_inference_avec_cache(payload: RequeteIA):
    cle_recherche = payload.user_prompt.strip().lower()
    temps_actuel = time.time()
    
    if cle_recherche in api_cache_storage:
        cache_data = api_cache_storage[cle_recherche]
        if temps_actuel - cache_data["cached_at"] < CACHE_TTL_SECONDS:
            return {
                "llm_response": cache_data["response"],
                "cache_hit": True,
                "execution_time_ms": 0.0,
                "source": "MEMORY_CACHE_ACCELERATOR"
            }
            
    start_time = time.time()
    time.sleep(1.2)  # Inférence artificielle
    simulated_output = f"Résultat de l'analyse sémantique pour : '{payload.user_prompt}'"
    end_time = time.time()
    execution_latency = round((end_time - start_time) * 1000, 2)
    
    api_cache_storage[cle_recherche] = {
        "response": simulated_output,
        "cached_at": temps_actuel
    }
    
    return {
        "llm_response": simulated_output,
        "cache_hit": False,
        "execution_time_ms": execution_latency,
        "source": "HEAVY_COMPUTATION_ENGINE"
    }
