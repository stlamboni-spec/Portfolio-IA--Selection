import asyncio
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

# 1. Initialisation de l'application Multi-Agents
app = FastAPI(
    title="Multi-Agent Task Orchestrator",
    description="Core GenAI Engine: Intelligent routing powered by Qwen orchestrations.",
    version="1.0.0"
)

class AgentQueryRequest(BaseModel):
    user_query: str = Field(..., description="La requête ou question de l'utilisateur.")

class AgentRoutingResponse(BaseModel):
    selected_agent: str
    confidence_score: float
    agent_execution_output: str
    message: str

# Simulation des comportements d'agents spécialisés (Simulated Local LLM Workers)
def execute_financial_agent(query: str) -> str:
    return f"[Financial Expert Response] Analysis completed for query '{query}'. Calculation of ROI and ARR yields a healthy 14% growth index."

def execute_technical_agent(query: str) -> str:
    return f"[DevOps/SRE Expert Response] Infrastructure check complete. Manifests for Helm deployment on your Kubernetes cluster are valid."

def execute_general_agent(query: str) -> str:
    return f"[General Assistant Response] I processed your request: '{query}'. Let me know if you need specific deep-dive metrics."

@app.post("/api/v1/agents/route", response_model=AgentRoutingResponse)
async def route_llm_task(request: AgentQueryRequest):
    """
    Routeur sémantique simulant une classification de prompt à la volée.
    Aiguille la requête vers l'agent expert approprié.
    """
    query_lower = request.user_query.lower()
    
    # Logique de routage sémantique basée sur les mots-clés
    if any(word in query_lower for word in ["financier", "roi", "budget", "chiffre", "argent"]):
        selected = "Financial_Specialist_Agent"
        output = execute_financial_agent(request.user_query)
        score = 0.95
    elif any(word in query_lower for word in ["kubernetes", "docker", "pipeline", "code", "infra", "port"]):
        selected = "Tech_Infrastructure_Agent"
        output = execute_technical_agent(request.user_query)
        score = 0.98
    else:
        selected = "General_Purpose_Agent"
        output = execute_general_agent(request.user_query)
        score = 0.85

    return AgentRoutingResponse(
        selected_agent=selected,
        confidence_score=score,
        agent_execution_output=output,
        message=f"La requête a été routée de manière dynamique vers {selected}."
    )

# 2. Utilisation de TestClient pour valider le comportement dans Colab
client = TestClient(app)

print("=== SYSTÈME MULTI-AGENTS GÉNÉRATIF (SIMULATION INÉDITE) ===")

# Scénarios de tests
requetes = [
    "Quel est le ROI de notre campagne et le budget restant ?",
    "Peux-tu vérifier mon fichier docker-compose et mon pipeline ?",
    "Bonjour ! Raconte-moi une blague sur les développeurs."
]

for idx, req in enumerate(requetes, 1):
    response = client.post("/api/v1/agents/route", json={"user_query": req})
    data = response.json()
    print(f"\n[Test #{idx}] Requête client : '{req}'")
    print(f"         -> Agent Sélectionné : {data['selected_agent']} (Confiance : {data['confidence_score']})")
    print(f"         -> Sortie LLM Agent : {data['agent_execution_output']}")

        
