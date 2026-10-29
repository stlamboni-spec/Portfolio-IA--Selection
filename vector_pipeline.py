fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import numpy as np

# 1. Initialisation de l'API pour le Pipeline 4 (Vector DB)
app = FastAPI(
    title="Pipeline 4 : Enterprise Vector Database Indexer Microservice",
    description="Microservice simulant une base de données vectorielle (Qdrant/Chroma) pour la recherche sémantique par similarité de Cosinus.",
    version="1.0.0"
)

print("🧠 Moteur d'indexation vectorielle opérationnel en production !")

# Base vectorielle persistée en mémoire (Embeddings latents de 5 dimensions)
vector_database = {
    "doc_1_urban_planning": np.array([0.15, 0.88, -0.23, 0.45, 0.02]),
    "doc_2_credit_scoring": np.array([-0.72, 0.11, 0.64, -0.12, 0.55]),
    "doc_3_multi_agents":   np.array([0.05, -0.34, 0.12, 0.91, -0.18]),
}

class RequeteRechercheVectorielle(BaseModel):
    query_text: str = Field(
        ..., 
        json_schema_extra={"example": "Analyse de l'aménagement du territoire et étalement urbain."}
    )

def calculer_similarite_vecteurs(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return float(dot_product / (norm_v1 * norm_v2)) if norm_v1 and norm_v2 else 0.0

# 2. Endpoint de recherche sémantique avancée
@app.post("/vector_search", summary="Recherche sémantique par similarité cosinus au sein des embeddings")
def effectuer_recherche_vectorielle(donnees: RequeteRechercheVectorielle):
    try:
        # Génération déterministe d'embeddings basée sur le contexte textuel
        if "urbain" in donnees.query_text.lower() or "territorial" in donnees.query_text.lower():
            query_embedding = np.array([0.12, 0.82, -0.20, 0.41, 0.05])
        else:
            query_embedding = np.array([0.02, -0.30, 0.15, 0.85, -0.12])
            
        meilleur_score = -1.0
        meilleur_document_id = None
        
        for doc_id, doc_vector in vector_database.items():
            score = calculer_similarite_vecteurs(query_embedding, doc_vector)
            if score > meilleur_score:
                meilleur_score = score
                meilleur_document_id = doc_id
                
        return {
            "user_query_text": donnees.query_text,
            "simulated_query_embeddings": query_embedding.tolist(),
            "matched_document_id": meilleur_document_id,
            "vector_database_score": round(meilleur_score, 4),
            "status": "VECTOR_MATCH_SUCCESS"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'indexation vectorielle : {str(e)}")
