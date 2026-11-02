from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import time

# Initialisation de l'API pour le Pipeline 16 (Async Logging)
app = FastAPI(
    title="Pipeline 16 : Enterprise Async Logging Shield Microservice",
    description="Microservice de journalisation asynchrone découplé gérant l'écriture de logs système en tâche de fond pour optimiser la latence d'inférence de l'API principale.",
    version="1.0.0"
)

# Registre mémoire simulant la persistance sur disque
async_logs_storage = []

class RequeteInference(BaseModel):
    prompt_text: str

def worker_ecriture_logs(task_id: str, prompt: str, latency_ms: float):
    time.sleep(0.2)  # Simulation du coût d'écriture E/S disque
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "task_id": task_id,
        "logged_prompt": prompt,
        "inference_latency_ms": latency_ms,
        "status": "LOG_PERSISTED_SUCCESSFULLY"
    }
    async_logs_storage.append(log_entry)

@app.post("/inference_and_log", summary="Exécuter l'inférence IA et déléguer la journalisation au pool de workers")
def executer_ia_et_journaliser(payload: RequeteInference, background_tasks: BackgroundTasks):
    start_time = time.time()
    
    # Simulation du traitement d'inférence (50ms)
    time.sleep(0.05)
    simulated_output = f"Résultat IA pour : '{payload.prompt_text}'"
    task_id = f"ai-task-{int(time.time())}"
    
    end_time = time.time()
    execution_latency = round((end_time - start_time) * 1000, 2)
    
    # Envoi de la tâche lourde au BackgroundTask Worker de FastAPI
    background_tasks.add_task(worker_ecriture_logs, task_id, payload.prompt_text, execution_latency)
    
    return {
        "task_id": task_id,
        "llm_output": simulated_output,
        "api_response_time_ms": execution_latency,
        "logging_status": "DELEGATED_TO_BACKGROUND_WORKER"
    }
