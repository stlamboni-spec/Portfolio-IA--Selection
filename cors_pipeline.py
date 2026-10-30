from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialisation de l'API pour le Pipeline 9 (CORS Shield)
app = FastAPI(
    title="Pipeline 9 : Enterprise CORS Shield Microservice",
    description="Microservice de sécurité réseau appliquant un bouclier CORS (Cross-Origin Resource Sharing) pour restreindre l'inférence aux seuls domaines de confiance.",
    version="1.0.0"
)

# Liste blanche des origines autorisées en production
ORIGINS_LIST_WHITE = [
    "https://stlamboni.dev",
    "https://portfolio.stlamboni.dev",
    "https://trusted-client-app.com"
]

# Application du middleware officiel FastAPI pour la protection CORS globale
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS_LIST_WHITE,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

class PromptSecurise(BaseModel):
    prompt_text: str

@app.post("/secure_inference", summary="Inférence LLM protégée par filtrage d'origine réseau")
def executer_inference_filtree(payload: PromptSecurise):
    return {
        "status": "ALLOWED",
        "message": "CORS validation passed. Origin infrastructure is trusted.",
        "simulated_output": f"Safe inference output for: '{payload.prompt_text}'"
    }
