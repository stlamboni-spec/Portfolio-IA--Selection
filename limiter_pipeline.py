import time
from collections import defaultdict
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

# 1. Initialisation directe de l'application de votre Portfolio
app = FastAPI(
    title="Volumetric Rate Limiter Shield",
    description="Network Protection Layer: Sliding-window HTTP 429 rate-limiting gate.",
    version="1.0.0"
)

# Configuration de la politique de sécurité : Max 3 requêtes par fenêtre de 10 secondes par IP/User
RATE_LIMIT_WINDOW_SECONDS = 10
MAX_REQUESTS_PER_WINDOW = 3

# Registre en mémoire pour suivre l'historique des horodatages (timestamps) des requêtes par utilisateur
traffic_registry = defaultdict(list)

class RateLimitCheckRequest(BaseModel):
    client_ip: str = Field(..., description="Adresse IP ou clé d'identification du client.")
    endpoint: str = Field(..., description="L'endpoint ciblé par le trafic.")

class LimiterResponse(BaseModel):
    allowed: bool
    current_requests: int
    window_seconds: int
    action: str
    message: str

@app.post("/api/security/limiter", response_model=LimiterResponse)
async def check_rate_limit(request: RateLimitCheckRequest):
    """
    Analyse les requêtes entrantes via un algorithme de fenêtre glissante.
    Élimine les anciens appels et bloque l'accès si le seuil volumétrique est dépassé.
    """
    client_key = request.client_ip
    current_time = time.time()
    
    # Nettoyage : On ne garde que les requêtes effectuées dans la fenêtre de temps active (10s)
    traffic_registry[client_key] = [
        timestamp for timestamp in traffic_registry[client_key]
        if current_time - timestamp < RATE_LIMIT_WINDOW_SECONDS
    ]
    
    # Vérification du seuil
    request_count = len(traffic_registry[client_key])
    
    if request_count >= MAX_REQUESTS_PER_WINDOW:
        # Blocage immédiat du trafic abusif
        return LimiterResponse(
            allowed=False,
            current_requests=request_count,
            window_seconds=RATE_LIMIT_WINDOW_SECONDS,
            action="DENIED_HTTP_429",
            message=f"Trafic bloqué : Seuil dépassé ({request_count}/{MAX_REQUESTS_PER_WINDOW} requêtes). Veuillez patienter."
        )
    
    # Enregistrement de la requête légitime actuelle
    traffic_registry[client_key].append(current_time)
    updated_count = len(traffic_registry[client_key])
    
    return LimiterResponse(
        allowed=True,
        current_requests=updated_count,
        window_seconds=RATE_LIMIT_WINDOW_SECONDS,
        action="ALLOWED",
        message="Requête autorisée sous les seuils de sécurité de l'infrastructure."
    )

# 2. Création du client de test interne (TestClient) pour éviter les blocages de ports
client = TestClient(app)

# 3. Simulation d'un trafic agressif pour tester le pare-feu
client_ip_test = "192.168.1.50"
payload = {"client_ip": client_ip_test, "endpoint": "/api/v1/chat/completions"}

print("=== SÉCURISATION RÉSEAU : SIMULATION DE DOS / BRUTE-FORCE ===")

# Envoi rapide de 5 requêtes consécutives pour saturer le limiteur
for i in range(1, 6):
    response = client.post("/api/security/limiter", json=payload)
    res_data = response.json()
    
    status_msg = "✅ APPROUVÉ" if res_data["allowed"] else "❌ BLOQUÉ (HTTP 429)"
    print(f"Requête #{i} | Statut: {status_msg} | Total dans la fenêtre: {res_data['current_requests']} | Msg: {res_data['message']}")
