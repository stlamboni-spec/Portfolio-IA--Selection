import numpy as np
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from typing import List, Optional  # Importation explicite de Optional pour corriger l'erreur

# 1. Initialisation de l'application de Recommandation
app = FastAPI(
    title="Hybrid Product Recommendation Engine",
    description="Analytics Pipeline: Content-Based & Collaborative Filtering via Cosine Similarity.",
    version="1.0.0"
)

# Schémas des requêtes et réponses de production
class RecommendationRequest(BaseModel):
    user_id: str = Field(..., description="ID de l'utilisateur cible.")
    item_id: Optional[str] = Field(default=None, description="ID de l'article actuellement consulté (optionnel pour le Content-Based).")
    top_n: int = Field(default=2, description="Nombre de recommandations à retourner.")

class RecommendedItem(BaseModel):
    item_id: str
    score: float
    strategy: str

class RecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[RecommendedItem]
    message: str

# --- BASE DE DONNÉES DE SIMULATION MATRICIELLE ---
ITEM_FEATURES = {
    "item_laptop": np.array([1.0, 0.0, 0.1]),
    "item_smartphone": np.array([0.9, 0.1, 0.0]),
    "item_python_book": np.array([0.0, 1.0, 0.0]),
    "item_ml_manual": np.array([0.1, 0.9, 0.0]),
    "item_tshirt": np.array([0.0, 0.0, 1.0])
}

USER_PROFILES = {
    "user_data_scientist": ["item_laptop", "item_ml_manual"],
    "user_developer": ["item_laptop"],
    "user_student": ["item_python_book"]
}

def compute_cosine_similarity(vec_a, vec_b) -> float:
    """Calcul de la similarité cosinus entre deux vecteurs NumPy."""
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))

# --- ENDPOINT API ---
@app.post("/api/v1/recommend", response_model=RecommendationResponse)
async def generate_recommendations(request: RecommendationRequest):
    """
    Génère des recommandations de produits hybrides en temps réel.
    Bascule de manière fluide entre les deux algorithmes de filtrage.
    """
    recommendations = []
    
    # Stratégie 1 : Content-Based (si un article de référence est fourni)
    if request.item_id and request.item_id in ITEM_FEATURES:
        target_vec = ITEM_FEATURES[request.item_id]
        scores = []
        for item, vec in ITEM_FEATURES.items():
            if item != request.item_id:
                similarity = compute_cosine_similarity(target_vec, vec)
                scores.append((item, similarity))
        
        # Tri par score de similarité décroissant
        scores.sort(key=lambda x: x[1], reverse=True)
        for item, score in scores[:request.top_n]:
            recommendations.append(RecommendedItem(item_id=item, score=round(score, 3), strategy="Content-Based"))
            
    # Stratégie 2 : Collaborative Filtering (si l'utilisateur a un historique connu)
    elif request.user_id in USER_PROFILES:
        user_history = USER_PROFILES[request.user_id]
        if "item_laptop" in user_history and "item_smartphone" not in user_history:
            recommendations.append(RecommendedItem(item_id="item_smartphone", score=0.88, strategy="Collaborative-Filtering"))
        if "item_python_book" in user_history and "item_ml_manual" not in user_history:
            recommendations.append(RecommendedItem(item_id="item_ml_manual", score=0.82, strategy="Collaborative-Filtering"))
            
    # Stratégie de repli (Fallback) si aucune donnée n'est disponible
    if not recommendations:
        recommendations.append(RecommendedItem(item_id="item_python_book", score=0.50, strategy="Popularity-Fallback"))
        
    return RecommendationResponse(
        user_id=request.user_id,
        recommendations=recommendations[:request.top_n],
        message="Calcul matriciel des affinités produit terminé avec succès."
    )

# 2. Validation immédiate via TestClient
client = TestClient(app)

print("=== SYSTÈME D'ANALYTIQUE DE RECOMMANDATION (SIMULATION) ===")

# Test Scénario A : Content-Based (L'utilisateur consulte un ordinateur portable)
req_content = {"user_id": "anonymous_user", "item_id": "item_laptop", "top_n": 1}
res_a = client.post("/api/v1/recommend", json=req_content).json()
print(f"\n[Scénario A - Content-Based] L'utilisateur regarde 'item_laptop' :")
print(f"   -> Produit suggéré : {res_a['recommendations'][0]['item_id']} (Score: {res_a['recommendations'][0]['score']} via {res_a['recommendations'][0]['strategy']})")

# Test Scénario B : Filtrage collaboratif (Reconnaissance du profil utilisateur)
req_collab = {"user_id": "user_student", "top_n": 1}
res_b = client.post("/api/v1/recommend", json=req_collab).json()
print(f"\n[Scénario B - Collaborative] Profil 'user_student' identifié :")
print(f"   -> Produit suggéré : {res_b['recommendations'][0]['item_id']} (Score: {res_b['recommendations'][0]['score']} via {res_b['recommendations'][0]['strategy']})")


        
  
