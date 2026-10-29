rom fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

# Initialisation de l'API pour le Pipeline 5 (Monitoring)
app = FastAPI(
    title="Pipeline 5 : Real-Time AI Metrics Monitor Microservice",
    description="Microservice industriel d'exposition de métriques MLOps au format Prometheus/Grafana pour suivre la latence et la consommation de jetons.",
    version="1.0.0"
)

# Registre de métriques en mémoire de production
metrics_registry = {
    "total_inference_requests": 0,
    "total_tokens_consumed": 0,
    "latency_histogram_ms": [],
    "http_error_counter": 0
}

class PromptInference(BaseModel):
    text: str

@app.post("/monitored_inference", summary="Endpoint d'inférence avec calcul en temps réel des métriques logicielles")
def executer_inference_suivie(donnees: PromptInference):
    temps_debut = time.time()
    try:
        if not donnees.text.strip():
            metrics_registry["http_error_counter"] += 1
            raise HTTPException(status_code=400, detail="Le prompt fourni est vide.")
            
        # Simulation d'un traitement d'inférence
        time.sleep(0.12)
        
        temps_fin = time.time()
        latence_ms = round((temps_fin - temps_debut) * 1000, 2)
        tokens_estimes = len(donnees.text.split()) + 20
        
        metrics_registry["total_inference_requests"] += 1
        metrics_registry["total_tokens_consumed"] += tokens_estimes
        metrics_registry["latency_histogram_ms"].append(latence_ms)
        
        return {
            "status": "success",
            "latency_ms": latence_ms,
            "tokens_billed": tokens_estimes
        }
    except Exception as e:
        if not isinstance(e, HTTPException):
            metrics_registry["http_error_counter"] += 1
        raise e

@app.get("/metrics", summary="Route d'extraction des logs pour Prometheus et Grafana")
def extraire_metriques_historiques():
    total_req = metrics_registry["total_inference_requests"]
    latences = metrics_registry["latency_histogram_ms"]
    latence_moyenne = round(sum(latences) / total_req, 2) if total_req > 0 else 0.0
    
    return {
        "ai_requests_total": total_req,
        "ai_tokens_consumed_total": metrics_registry["total_tokens_consumed"],
        "ai_avg_latency_milliseconds": latence_moyenne,
        "ai_http_errors_total": metrics_registry["http_error_counter"],
        "monitoring_status": "HEALTHY"
    }
