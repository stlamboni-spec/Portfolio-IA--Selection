import asyncio
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict

# 1. Initialisation de l'application de Streaming d'Événements
app = FastAPI(
    title="Event-Driven Streaming Webhook Engine",
    description="Infrastructure Layer: Broadcasts asynchronous notifications to connected webhooks.",
    version="1.0.0"
)

# Registre des abonnements aux webhooks (In-Memory URL Database)
webhook_subscriptions: Dict[str, List[str]] = {
    "batch_completed": ["https://entreprise-tierce.com"],
    "security_alert": ["https://internal.net"]
}

class WebhookSubscriptionRequest(BaseModel):
    event_type: str = Field(..., description="Le type d'événement (ex: batch_completed, security_alert).")
    target_url: str = Field(..., description="L'URL de callback de l'application tierce.")

class EventPayload(BaseModel):
    event_id: str
    event_type: str
    data: dict

@app.post("/api/v1/webhooks/subscribe", status_code=status.HTTP_201_CREATED)
async def subscribe_to_event(request: WebhookSubscriptionRequest):
    """Permet à un service tiers de s'abonner à un flux d'événements du portfolio."""
    if request.event_type not in webhook_subscriptions:
        webhook_subscriptions[request.event_type] = []
    
    if request.target_url not in webhook_subscriptions[request.event_type]:
        webhook_subscriptions[request.event_type].append(request.target_url)
        
    return {"message": f"Inscription validée pour l'événement '{request.event_type}'."}

@app.post("/api/v1/webhooks/trigger", status_code=status.HTTP_202_ACCEPTED)
async def trigger_event_broadcast(payload: EventPayload):
    """
    Simule la diffusion (broadcast) asynchrone d'un événement MLOps.
    Parcourt le registre et notifie tous les récepteurs connectés.
    """
    event_type = payload.event_type
    urls_to_notify = webhook_subscriptions.get(event_type, [])
    
    print(f"\n[Moteur Webhook] Événement '{event_type}' détecté (ID: {payload.event_id}).")
    print(f"                 Diffusion en cours vers {len(urls_to_notify)} endpoint(s) externe(s)...")
    
    # En production, cela tourne dans un worker asynchrone (Celery/KEDA) avec httpx.AsyncClient()
    for url in urls_to_notify:
        print(f"                 -> Notification envoyée avec succès à : {url}")
        print(f"                 -> Données transmises : {payload.data}")
        
    return {"status": "broadcast_initiated", "notified_endpoints": len(urls_to_notify)}

# 2. Utilisation de TestClient pour valider l'infrastructure
client = TestClient(app)

print("=== ARCHITECTURE ÉVÉNEMENTIELLE : STREAMING DE WEBHOOKS ===")

# Test 1 : Inscription d'un nouveau serveur externe à nos alertes de sécurité
nouvel_abonnement = {
    "event_type": "security_alert",
    "target_url": "https://workspace.com"
}
client.post("/api/v1/webhooks/subscribe", json=nouvel_abonnement)

# Test 2 : Déclenchement d'une alerte (Simulation : le Guardrail bloque une attaque et lève un événement)
alerte_payload = {
    "event_id": "evt_99882233",
    "event_type": "security_alert",
    "data": {
        "source_ip": "192.168.1.105",
        "severity": "CRITICAL",
        "reason": "Prompt Injection Blocked by Guardrail"
    }
}
client.post("/api/v1/webhooks/trigger", json=alerte_payload)

   
