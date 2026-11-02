from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

# Initialisation de l'API pour le Pipeline 20 (Rate Limiter Gate)
app = FastAPI(
    title="Pipeline 20 : Enterprise Rate Limiter Gate Microservice",
    description="Microservice défensif limitant le débit volumétrique des requêtes par adresse IP (Redis-like design) pour contrer les attaques DDoS et le gaspillage de tokens.",
    version="1.0.0"
)

rate_limit_records = {}
MAX_REQUESTS_PER_WINDOW = 2
WINDOW_DURATION_SECONDS = 10

class PromptInference(BaseModel):
    prompt: str

def verifier_limite_de_debit(ip_client: str):
    import time
    temps_actuel = time.time()
    
    if ip_client not in rate_limit_records:
        rate_limit_records[ip_client] = []
        
    rate_limit_records[ip_client] = [
        ts for ts in rate_limit_records[ip_client] 
        if temps_actuel - ts < WINDOW_DURATION_SECONDS
    ]
    
    if len(rate_limit_records[ip_client]) >= MAX_REQUESTS_PER_WINDOW:
        le_plus_ancien_ts = rate_limit_records[ip_client][0]
        temps_attente_restant = round(WINDOW_DURATION_SECONDS - (temps_actuel - le_plus_ancien_ts), 1)
        raise HTTPException(
            status_code=429, 
            detail=f"Too Many Requests: Rate limit exceeded for IP '{ip_client}'. Retry after {temps_attente_restant}s."
        )
        
    rate_limit_records[ip_client].append(temps_actuel)

@app.post("/limited_inference", summary="Inférence sécurisée avec validation du quota volumétrique par IP")
def executer_inference_protegee(payload: PromptInference, request: Request):
    ip_simulee = request.headers.get("x-forwarded-for", "127.0.0.1")
    verifier_limite_de_debit(ip_simulee)
    
    return {
        "status": "REQUEST_ALLOWED",
        "client_ip": ip_simulee,
        "current_window_load": len(rate_limit_records[ip_simulee]),
        "message": f"Inference processing authorized for: '{payload.prompt}'"
    }
