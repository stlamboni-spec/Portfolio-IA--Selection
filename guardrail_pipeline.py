from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialisation de l'API pour le Pipeline 17 (Guardrail Gate)
app = FastAPI(
    title="Pipeline 17 : LLM Cost & Token Guardrail Gate Microservice",
    description="Microservice de sécurité et de contrôle financier interceptant les requêtes pour calculer le coût des tokens et bloquer les injections de prompts.",
    version="1.0.0"
)

PRICE_PER_TOKEN_USD = 0.000015
MAX_BUDGET_PER_REQUEST_USD = 0.0003

# Liste noire contre les injections de prompts malveillantes
PROMPT_INJECTION_BLACKLIST = ["ignore prior instructions", "ignore les instructions", "system override"]

class PromptPayload(BaseModel):
    user_prompt: str

@app.post("/guardrail_check", summary="Vérification de sécurité et de budget avant l'inférence LLM")
def verifier_cout_et_securite(payload: PromptPayload):
    prompt_nettoye = payload.user_prompt.lower().strip()
    
    # 1. Protection contre les injections de prompts
    for attack_keyword in PROMPT_INJECTION_BLACKLIST:
        if attack_keyword in prompt_nettoye:
            raise HTTPException(
                status_code=403, 
                detail="SECURITY_VIOLATION: Prompt injection attempt detected. Request aborted."
            )
            
    # 2. Calcul des jetons et estimation du coût financier
    estimated_tokens = len(prompt_nettoye.split()) + 15
    estimated_cost_usd = round(estimated_tokens * PRICE_PER_TOKEN_USD, 6)
    
    # 3. Vérification du garde-fou budgétaire
    if estimated_cost_usd > MAX_BUDGET_PER_REQUEST_USD:
        raise HTTPException(
            status_code=402, 
            detail=f"BUDGET_EXCEEDED: Estimated cost ${estimated_cost_usd} exceeds request limit."
        )
        
    return {
        "status": "GUARDRAIL_PASSED",
        "tokens_count": estimated_tokens,
        "estimated_cost_usd": estimated_cost_usd,
        "security_check": "CLEAN"
    }
