import time
import uuid
from typing import List, Dict, Optional
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="LLM LoRA Fine-Tuning & Evaluation Pipeline",
    description="Microservice d'orchestration pour le fine-tuning léger (PEFT/LoRA) et le suivi des métriques.",
    version="1.0.0"
)

# Stockage en mémoire des jobs d'entraînement (remplaçable par Redis/PostgreSQL)
training_jobs: Dict[str, dict] = {}


# --- 1. Schémas de validation stricts (Pydantic v2) ---
class TrainingSample(BaseModel):
    instruction: str = Field(..., min_length=5, description="Prompt ou question métier")
    response: str = Field(..., min_length=2, description="Réponse attendue du modèle")


class LoRAConfigRequest(BaseModel):
    base_model: str = Field(default="Qwen/Qwen2.5-3B-Instruct", description="Modèle HuggingFace de base")
    lora_r: int = Field(default=16, ge=4, le=128, description="Rang des matrices LoRA (Low-Rank)")
    lora_alpha: int = Field(default=32, ge=8, le=256, description="Facteur d'échelle LoRA")
    lora_dropout: float = Field(default=0.05, ge=0.0, le=0.5)
    quantization_4bit: bool = Field(default=True, description="Activer QLoRA (4-bit bitsandbytes)")
    epochs: int = Field(default=3, ge=1, le=20)
    learning_rate: float = Field(default=2e-4, gt=0.0, lt=1.0)
    dataset: List[TrainingSample] = Field(..., min_length=2, description="Jeu de données d'entraînement")


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    base_model: str
    trainable_params_ratio: str
    metrics: Optional[Dict[str, float]] = None


# --- 2. Tâche d'entraînement asynchrone (Simulation PEFT / SFTTrainer) ---
def run_lora_training_task(job_id: str, config: LoRAConfigRequest):
    training_jobs[job_id]["status"] = "RUNNING"
    
    # Calcul théorique de l'économie de paramètres grâce à LoRA (~0.8% à 1.5% des poids)
    trainable_ratio = round((config.lora_r / 2048) * 100, 2)
    training_jobs[job_id]["trainable_params_ratio"] = f"{trainable_ratio}%"

    # Simulation des epochs d'entraînement (remplaçable par trl.SFTTrainer sur GPU)
    current_loss = 2.45
    for epoch in range(1, config.epochs + 1):
        time.sleep(1.5)  # Simule le calcul sur GPU
        current_loss = round(current_loss * 0.68, 4)
        training_jobs[job_id]["metrics"] = {
            "current_epoch": epoch,
            "train_loss": current_loss,
            "eval_perplexity": round(2.718 ** current_loss, 2)
        }

    training_jobs[job_id]["status"] = "COMPLETED"


# --- 3. Endpoints API ---
@app.post("/api/v1/finetune/lora", response_model=JobStatusResponse, status_code=202)
async def start_lora_finetuning(config: LoRAConfigRequest, background_tasks: BackgroundTasks):
    """
    Lance un job asynchrone de fine-tuning QLoRA/LoRA et retourne un identifiant de suivi.
    """
    job_id = str(uuid.uuid4())[:8]
    training_jobs[job_id] = {
        "job_id": job_id,
        "status": "QUEUED",
        "base_model": config.base_model,
        "trainable_params_ratio": "Calculating...",
        "metrics": None
    }

    background_tasks.add_task(run_lora_training_task, job_id, config)
    return training_jobs[job_id]


@app.get("/api/v1/finetune/status/{job_id}", response_model=JobStatusResponse)
async def get_training_status(job_id: str):
    """
    Permet de suivre l'évolution de la loss et de la perplexité en temps réel.
    """
    if job_id not in training_jobs:
        raise HTTPException(status_code=404, detail="Job de fine-tuning introuvable.")
    return training_jobs[job_id]


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "lora-finetuning-pipeline"}
