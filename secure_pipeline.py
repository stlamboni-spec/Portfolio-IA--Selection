import time
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# 1. Initialisation de l'API pour le Pipeline 3 (Plomberie Backend)
app = FastAPI(
    title="Pipeline 3 : Secure AI Microservice Template",
    description="Squelette industriel d'API sécurisé par clé API, middleware CORS restrictif et protection par Rate Limiting.",
    version="1.0.0"
)

# 2. Configuration défensive : Clé API & Restriction CORS
API_KEY_SECRET = "sk_prod_togomlops_2026"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À remplacer par vos domaines de production réels
    allow_credentials=True,
    allow_methods=["POST"],  # Uniquement autoriser les requêtes POST d'inférence
    allow_headers=["X-API-Key", "Content-Type"],
)

# Système de Rate Limiting en mémoire
historique_requetes = {}

def valider_securite_et_rate_limit(api_key: str = Depends(api_key_header)):
    # Vérification de l'authentification
    if api_key != API_KEY_SECRET:
        raise HTTPException(status_code=403, detail="Authentification échouée : Clé API invalide ou manquante.")
    
    # Limitation : Max 5 requêtes toutes les 10 secondes en production
    temps_actuel = time.time()
    if api_key not in historique_requetes:
        historique_requetes[api_key] = []
        
    historique_requetes[api_key] = [t for t in historique_requetes[api_key] if temps_actuel - t < 10]
    
    if len(historique_requetes[api_key]) >= 5:
        raise HTTPException(status_code=429, detail="Trop de requêtes (Rate Limit dépassé). Veuillez patienter.")
        
    historique_requetes[api_key].append(temps_actuel)

# 3. Schéma de données strict avec validation Pydantic v2
class DemandeInference(BaseModel):
    prompt: str = Field(
        ..., 
        json_schema_extra={"example": "Analyse de sentiment pour cette réclamation client informatique."}
    )

# 4. Route Sécurisée d'Inférence Protectrice
@app.post("/secure_inference", dependencies=[Depends(valider_securite_et_rate_limit)], summary="Endpoint d'inférence hautement sécurisé")
def executer_inference_securisee(donnees: DemandeInference):
    try:
        return {
            "status": "authenticated_and_secured",
            "input_prompt": donnees.prompt,
            "api_shield_logs": "CORS cleared, API Key token matching, Rate Limit verified successfully."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du bouclier de sécurité : {str(e)}")
