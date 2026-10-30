from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
import uuid
import time

# Initialisation de l'API pour le Pipeline 6 (Batch Processing)
app = FastAPI(
    title="Pipeline 6 : Enterprise Batch Inference Engine Microservice",
    description="Microservice asynchrone découplé gérant le traitement par lots (Batch Processing) de prompts IA avec système de file d'attente et worker en tâche de fond.",
    version="1.0.0"
)

# Base de données volatile simulant un courtier de messages (Message Broker / Redis layout)
tasks_database = {}

class BatchInferencePayload(BaseModel):
    prompts: list[str] = Field(..., json_schema_extra={"example": ["Analyse urbaine", "Optimisation foncière"]})

def backend_inference_worker(task_id: str, prompts: list[str]):
    tasks_database[task_id]["status"] = "PROCESSING"
    results = []
    
    for idx, prompt in enumerate(prompts):
        time.sleep(0.1)  # Simulation du coût d'inférence LLM
        results.append({
            "prompt_index": idx,
            "raw_prompt": prompt,
            "simulated_llm_output": f"Processed batch result for: '{prompt}'",
            "processed_at": time.strftime("%H:%M:%S")
        })
        
    tasks_database[task_id]["status"] = "COMPLETED"
    tasks_database[task_id]["results"] = results
    tasks_database[task_id]["completed_at"] = time.strftime("%H:%M:%S")

@app.post("/batch_submit", status_code=202, summary="Soumettre un lot de prompts à traiter de manière asynchrone (Non-bloquant)")
def soumettre_un_lot_ia(payload: BatchInferencePayload, background_tasks: BackgroundTasks):
    if not payload.prompts:
        raise HTTPException(status_code=400, detail="La liste de prompts ne peut pas être vide.")
        
    task_id = str(uuid.uuid4())
    tasks_database[task_id] = {
        "task_id": task_id,
        "status": "QUEUED",
        "total_prompts": len(payload.prompts),
        "results": [],
        "created_at": time.strftime("%H:%M:%S")
    }
    
    background_tasks.add_task(backend_inference_worker, task_id, payload.prompts)
    
    return {
        "message": "Batch job submitted successfully to the background worker pool.",
        "task_id": task_id,
        "check_status_url": f"/batch_status/{task_id}"
    }

@app.get("/batch_status/{task_id}", summary="Interroger le statut et récupérer les résultats d'un lot (Polling)")
def verifier_statut_du_lot(task_id: str):
    if task_id not in tasks_database:
        raise HTTPException(status_code=404, detail="L'identifiant de tâche fourni est introuvable.")
    return tasks_database[task_id]
