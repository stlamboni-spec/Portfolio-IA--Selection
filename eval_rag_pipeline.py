import re
from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="RAG vs Base LLM Comparative Evaluation Pipeline",
    description="Microservice d'évaluation de la fidélité (anti-hallucination), de la pertinence et de la latence entre un LLM nu et un pipeline RAG.",
    version="1.0.0"
)


# --- 1. Schémas de validation stricts (Pydantic v2) ---
class EvaluationSample(BaseModel):
    question: str = Field(..., min_length=5, description="Question posée par l'utilisateur")
    ground_truth_context: str = Field(..., min_length=10, description="Document source de référence (vérité terrain)")
    base_llm_answer: str = Field(..., min_length=2, description="Réponse générée par le LLM seul (sans RAG)")
    rag_answer: str = Field(..., min_length=2, description="Réponse générée par le pipeline RAG")
    base_llm_latency_ms: float = Field(default=320.0, gt=0)
    rag_latency_ms: float = Field(default=480.0, gt=0)


class BatchEvaluationRequest(BaseModel):
    model_name: str = Field(default="Qwen/Qwen2.5-3B-Instruct")
    samples: List[EvaluationSample] = Field(..., min_length=1)


class SampleMetricResult(BaseModel):
    question: str
    base_llm_faithfulness: float
    rag_faithfulness: float
    hallucination_risk_base: str
    hallucination_risk_rag: str
    accuracy_gain_pct: float


class ComparativeReportResponse(BaseModel):
    model_name: str
    total_samples: int
    avg_base_faithfulness: float
    avg_rag_faithfulness: float
    avg_base_latency_ms: float
    avg_rag_latency_ms: float
    recommendation: str
    details: List[SampleMetricResult]


# --- 2. Moteur de calcul des métriques de fidélité ---
def _tokenize(text: str) -> set:
    words = re.findall(r"\b[a-zA-ZÀ-ÿ0-9]{3,}\b", text.lower())
    stopwords = {"les", "des", "une", "dans", "pour", "avec", "sur", "par", "est", "sont", "que", "qui", "the", "and", "for", "with"}
    return {w for w in words if w not in stopwords}


def compute_faithfulness_score(answer: str, context: str) -> float:
    """
    Mesure la proportion des concepts clés de la réponse qui sont réellement ancrés
    dans le document source (score entre 0.0 et 1.0).
    """
    answer_tokens = _tokenize(answer)
    context_tokens = _tokenize(context)
    if not answer_tokens:
        return 0.0
    supported_tokens = answer_tokens.intersection(context_tokens)
    return round(len(supported_tokens) / len(answer_tokens), 4)


def classify_hallucination_risk(faithfulness: float) -> str:
    if faithfulness >= 0.70:
        return "LOW (Grounded)"
    elif faithfulness >= 0.40:
        return "MEDIUM (Partial)"
    return "HIGH (Likely Hallucination)"


# --- 3. Endpoint d'évaluation comparative ---
@app.post("/api/v1/evaluate/compare", response_model=ComparativeReportResponse)
async def compare_rag_vs_llm(request: BatchEvaluationRequest):
    """
    Évalue un jeu de test pour comparer un LLM seul face à un pipeline RAG
    sur la fidélité aux sources et le compromis latence/précision.
    """
    results: List[SampleMetricResult] = []
    total_base_faith = 0.0
    total_rag_faith = 0.0
    total_base_lat = 0.0
    total_rag_lat = 0.0

    for item in request.samples:
        base_score = compute_faithfulness_score(item.base_llm_answer, item.ground_truth_context)
        rag_score = compute_faithfulness_score(item.rag_answer, item.ground_truth_context)
        gain = round((rag_score - base_score) * 100, 2)

        total_base_faith += base_score
        total_rag_faith += rag_score
        total_base_lat += item.base_llm_latency_ms
        total_rag_lat += item.rag_latency_ms

        results.append(SampleMetricResult(
            question=item.question,
            base_llm_faithfulness=base_score,
            rag_faithfulness=rag_score,
            hallucination_risk_base=classify_hallucination_risk(base_score),
            hallucination_risk_rag=classify_hallucination_risk(rag_score),
            accuracy_gain_pct=gain
        ))

    n = len(request.samples)
    avg_base = round(total_base_faith / n, 4)
    avg_rag = round(total_rag_faith / n, 4)
    avg_base_lat = round(total_base_lat / n, 1)
    avg_rag_lat = round(total_rag_lat / n, 1)

    if avg_rag > avg_base + 0.15:
        rec = "DEPLOY RAG: Gain majeur de fidélité documentaire et réduction significative des hallucinations."
    elif avg_rag > avg_base:
        rec = "HYBRID / RAG RECOMMENDED: Amélioration modérée ; envisagez un affinage du chunking ou un fine-tuning LoRA."
    else:
        rec = "BASE / FINE-TUNED LLM SUFFICIENT: Le modèle maîtrise déjà le domaine sans surcoût de latence RAG."

    return ComparativeReportResponse(
        model_name=request.model_name,
        total_samples=n,
        avg_base_faithfulness=avg_base,
        avg_rag_faithfulness=avg_rag,
        avg_base_latency_ms=avg_base_lat,
        avg_rag_latency_ms=avg_rag_lat,
        recommendation=rec,
        details=results
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "rag-vs-llm-evaluator"}
