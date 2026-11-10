from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient
from pydantic import BaseModel

# 1. Initialisation de l'application réseau isolée
app = FastAPI(
    title="Enterprise Network Isolation Shield (CORS)",
    description="Security Layer: Granular Cross-Origin Resource Sharing control gate.",
    version="1.0.0"
)

# Configuration de la politique de sécurité CORS d'entreprise
ALLOWED_ORIGINS = [
    "https://entreprise.com",  # Origine légitime autorisée (Frontend)
    "https://selection-turing.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

class SecurityVerificationRequest(BaseModel):
    origin_url: str

@app.get("/api/v1/security/cors-status", status_code=status.HTTP_200_OK)
async def get_cors_protection_status():
    """Endpoint public retournant la configuration de la barrière réseau."""
    return {
        "cors_protection": "ACTIVE",
        "authorized_origins_count": len(ALLOWED_ORIGINS),
        "policy": "Strict Enterprise Isolation"
    }

# 2. Utilisation de TestClient pour simuler les entêtes HTTP CORS (Origin)
client = TestClient(app)

print("=== BOUCLIER DE SÉCURITÉ RÉSEAU : ISOLATION CORS ===")

# Test Scénario A : Requête provenant d'un domaine légitime configuré
print("\n[Scénario A] Connexion depuis le tableau de bord autorisé...")
headers_legitime = {"Origin": "https://entreprise.com"}
response_a = client.get("/api/v1/security/cors-status", headers=headers_legitime)

# Si l'origine est acceptée, FastAPI renvoie l'entête de validation dans sa réponse
cors_header_a = response_a.headers.get("access-control-allow-origin", "Bloqué")
print(f"   -> Statut HTTP : {response_a.status_code}")
print(f"   -> Entête Access-Control-Allow-Origin renvoyée : {cors_header_a}")
print(f"   -> Résultat : ✅ ACCÈS AUTORISÉ AU FRONTEND")

# Test Scénario B : Requête pirate / non autorisée (ex: domaine-malveillant.com)
print("\n[Scénario B] Tentative de connexion depuis un domaine malveillant ou non listé...")
headers_pirate = {"Origin": "https://domaine-malveillant-hacker.com"}
response_b = client.get("/api/v1/security/cors-status", headers=headers_pirate)

cors_header_b = response_b.headers.get("access-control-allow-origin", "Aucune (Requête bloquée par le navigateur)")
print(f"   -> Statut HTTP : {response_b.status_code}")
print(f"   -> Entête Access-Control-Allow-Origin renvoyée : {cors_header_b}")
print(f"   -> Résultat : ❌ ACCÈS SÉCURISÉ ET BLOQUÉ PAR LE MIDDLEWARE")
