import time
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

# 1. Initialisation de l'application fusionnée Cache + Churn
app = FastAPI(
    title="Cache Accelerator & Churn Prediction Pipeline",
    description="Infrastructure & Analytics Layer: Low-latency caching and customer retention scoring.",
    version="1.0.0"
)

# --- BASE DE DONNÉES EN MÉMOIRE POUR LE CACHE SIMULÉ (REDIS LAYOUT) ---
cache_store = {}

class CacheRequest(BaseModel):
    key: str
    value: str
    ttl_seconds: int = 60

class ChurnRequest(BaseModel):
    user_id: str
    tenure_months: int = Field(..., ge=0)
    monthly_charges: float = Field(..., ge=0)
    support_tickets_opened: int = Field(..., ge=0)

# --- ENDPOINTS CACHE ---
@app.post("/api/v1/cache/set", status_code=status.HTTP_201_CREATED)
async def set_cache_value(request: CacheRequest):
    """Enregistre une paire clé-valeur avec un horodatage d'expiration."""
    cache_store[request.key] = {
        "value": request.value,
        "expires_at": time.time() + request.ttl_seconds
    }
    return {"status": "success", "message": f"Clé '{request.key}' mise en cache."}

@app.get("/api/v1/cache/get/{key}")
async def get_cache_value(key: str):
    """Récupère la valeur si elle existe et n'a pas expiré (Cache Hit vs Cache Miss)."""
    if key not in cache_store:
        return {"status": "miss", "value": None}
    
    entry = cache_store[key]
    if time.time() > entry["expires_at"]:
        del cache_store[key] # Nettoyage si expiré
        return {"status": "expired_miss", "value": None}
        
    return {"status": "hit", "value": entry["value"]}

# --- ENDPOINT CHURN (MACHINE LEARNING SIMULÉ) ---
@app.post("/api/v1/predict/churn", status_code=status.HTTP_200_OK)
async def predict_customer_churn(request: ChurnRequest):
    """
    Simule l'inférence d'un modèle de classification (type Random Forest / XGBoost).
    Calcule un score de risque de désabonnement basé sur les caractéristiques du client.
    """
    # Logique métier statistique linéaire/arbre décisionnel simplifiée
    score_facteur = (request.support_tickets_opened * 0.25) + (request.monthly_charges * 0.002) - (request.tenure_months * 0.01)
    
    # Normalisation du score entre 0.0 et 1.0 (Fonction Sigmoïde simulée)
    churn_probability = round(1 / (1 + math.exp(-score_facteur)) if 'math' in globals() else min(max(score_facteur, 0.0), 1.0), 3)
    
    risk_level = "Low"
    if churn_probability > 0.7:
        risk_level = "Critical"
    elif churn_probability > 0.4:
        risk_level = "Medium"
        
    return {
        "user_id": request.user_id,
        "churn_probability": churn_probability,
        "risk_level": risk_level,
        "action_recommended": "Trigger Retention Campaign" if risk_level in ["Medium", "Critical"] else "Maintain Standard Flow"
    }

# Ajout de l'import math manquant au cas où
import math

# 2. Validation instantanée avec TestClient
client = TestClient(app)

print("=== VERIFICATION DU CACHE ET DU PIPELINE DE CHURN ===")

# Test du Cache (Scénario In-Memory Accelerator)
print("\n[Test Cache] Écriture et lecture d'un résumé en cache...")
client.post("/api/v1/cache/set", json={"key": "summary_doc_1", "value": "Ceci est un résumé condensé de test."})
res_cache = client.get("/api/v1/cache/get/summary_doc_1").json()
print(f"   -> Statut du Cache : {res_cache['status']} | Valeur lue : \"{res_cache['value']}\"")

# Test du Churn (Scénario Client à Risque)
print("\n[Test Churn] Analyse d'un client insatisfait (beaucoup de tickets ouverts)...")
client_a_risque = {
    "user_id": "client_pro_88",
    "tenure_months": 3,
    "monthly_charges": 150.0,
    "support_tickets_opened": 6
}
res_churn = client.post("/api/v1/predict/churn", json=client_a_risque).json()
print(f"   -> Probabilité de départ : {res_churn['churn_probability']*100}%")
print(f"   -> Niveau de risque : {res_churn['risk_level']} | Action : {res_churn['action_recommended']}")
