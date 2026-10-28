from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import pipeline

# 1. Initialisation de l'API pour le Pipeline 2
app = FastAPI(
    title="Pipeline 2 : Multi-Agent Task Orchestrator Microservice",
    description="Microservice d'orchestration multi-agents automatisant la délégation de tâches à des sous-agents experts via LLM.",
    version="1.0.0"
)

print("🧠 Chargement du cerveau LLM pour l'Agent Manager (Qwen-0.5B-Chat)...")
generator_agents = pipeline("text-generation", model="Qwen/Qwen1.5-0.5B-Chat")
print("✅ Système Multi-Agents opérationnel en production !")

# Schéma de données avec typage défensif Pydantic v2
class DemandeMission(BaseModel):
    task_description: str = Field(
        ..., 
        json_schema_extra={"example": "Rédige une note de synthèse sur la sécurité informatique."}
    )

# 2. Logique métier des Agents Spécialisés
def agent_chercheur(critere: str):
    return f"[AGENT_RESEARCHER] Extraction et analyse des faits clés pour : '{critere}'."

def agent_ecrivain(contexte: str):
    return f"[AGENT_WRITER] Rédaction d'une ébauche textuelle professionnelle basée sur : '{contexte}'."

# 3. Endpoint de routage et d'orchestration
@app.post("/orchestrate", summary="Déléguer une tâche au meilleur agent disponible")
def orchestrer_mission(donnees: DemandeMission):
    try:
        mission = donnees.task_description.lower()
        
        # Routage déterministe de l'Agent Manager
        if "rédige" in mission or "ecris" in mission or "write" in mission:
            agent_cible = "Agent Écrivain ✍️"
            resultat_action = agent_ecrivain(donnees.task_description)
        else:
            agent_cible = "Agent Chercheur 🔍"
            resultat_action = agent_chercheur(donnees.task_description)
            
        # Synthèse managériale finale par le LLM (Formatage Transformers v5 strict)
        messages = [
            {
                "role": "user",
                "content": f"Tu es l'Agent Manager de l'équipe. Fais un rapport de synthèse très court de l'action entreprise : {resultat_action}"
            }
        ]
        
        outputs = generator_agents(messages, max_new_tokens=100, do_sample=False)
        synthese_finale = outputs["generated_text"][-1]["content"]
        
        return {
            "initial_task": donnees.task_description,
            "delegated_to": agent_cible,
            "raw_agent_output": resultat_action,
            "manager_synthesis": synthese_finale.strip()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'orchestration : {str(e)}")
