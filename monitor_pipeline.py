import time
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

# 1. Initialisation de l'application de Télémétrie et de Surveillance
app = FastAPI(
    title="Enterprise Monitoring & Telemetry Engine",
    description="Observability Layer: Core Prometheus/Grafana status and latency collector.",
    version="1.0.0"
)

# Registre en mémoire pour accumuler les métriques d'infrastructure
telemetry_registry = {
    "total_inference_requests": 0,
    "http_status_distribution": {200: 0, 429: 0, 500: 0},
    "latencies_ms": []
}

class TelemetryLogInput(BaseModel):
    endpoint: str = Field(..., description="L'URI du microservice surveillé.")
    execution_time_ms: float = Field(..., description="Temps de réponse de l'inférence en millisecondes.")
    http_status: int = Field(..., description="Code d'état HTTP retourné au client.")

@app.post("/api/v1/monitor/log", status_code=status.HTTP_200_OK)
async def log_pipeline_metrics(metrics: TelemetryLogInput):
    """
    Simule l'ingestion des métriques par un agent collecteur (Prometheus exporter).
    Agrège les temps de réponse et distribue les statuts HTTP du réseau.
    """
    telemetry_registry["total_inference_requests"] += 1
    
    status_code = metrics.http_status
    if status_code in telemetry_registry["http_status_distribution"]:
        telemetry_registry["http_status_distribution"][status_code] += 1
    else:
        telemetry_registry["http_status_distribution"][status_code] = 1
        
    telemetry_registry["latencies_ms"].append(metrics.execution_time_ms)
    
    return {"status": "metrics_ingested", "current_total": telemetry_registry["total_inference_requests"]}

@app.get("/metrics", summary="Endpoint de grattage pour Prometheus")
async def get_prometheus_metrics():
    """Expose les agrégats sous un format structuré lisible par Grafana/Prometheus."""
    latencies = telemetry_registry["latencies_ms"]
    avg_latency = round(sum(latencies) / len(latencies), 2) if latencies else 0.0
    
    return {
        "prometheus_metric_requests_total": telemetry_registry["total_inference_requests"],
        "prometheus_metric_http_status": telemetry_registry["http_status_distribution"],
        "prometheus_metric_average_latency_ms": avg_latency,
        "infrastructure_health": "GREEN"
    }

# 2. Utilisation de TestClient pour valider la collecte
client = TestClient(app)

print("=== INFRASTRUCTURE DE MONITORING ET TÉLÉMÉTRIE (GRAFANA/PROMETHEUS) ===")

# Simulation de l'ingestion de flux de télémétrie provenant de la Gateway et du Limiteur
logs_simulation = [
    {"endpoint": "/api/v1/chat/completions", "execution_time_ms": 124.5, "http_status": 200},
    {"endpoint": "/api/v1/chat/completions", "execution_time_ms": 142.1, "http_status": 200},
    {"endpoint": "/api/security/limiter", "execution_time_ms": 12.3, "http_status": 429}, # Bloqué par le Limiter
    {"endpoint": "/api/v21/index/batch", "execution_time_ms": 850.0, "http_status": 200}
]

print("-> Envoi des logs de performance au collecteur central...")
for log in logs_simulation:
    client.post("/api/v1/monitor/log", json=log)

# Récupération des données agrégées sur l'endpoint /metrics
print("\n-> Interrogation de l'endpoint Prometheus '/metrics' par Grafana :")
metrics_summary = client.get("/metrics").json()
print(f"   -> Nombre total de requêtes capturées : {metrics_summary['prometheus_metric_requests_total']}")
print(f"   -> Distribution des statuts HTTP réseau : {metrics_summary['prometheus_metric_http_status']}")
print(f"   -> Latence moyenne globale constatée : {metrics_summary['prometheus_metric_average_latency_ms']} ms")
print(f"   -> État de santé de la grappe cloud : {metrics_summary['infrastructure_health']}")

        
        
    
