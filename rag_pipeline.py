import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

# 1. Initialisation de l'API pour le Pipeline 1 (Projet Phare)
app = FastAPI(
    title="Pipeline 1 : Enterprise Production-Ready RAG Architecture",
    description="Microservice de génération augmentée par récupération (RAG) connectant une base de connaissances vectorielle à un LLM local.",
    version="1.0.0"
)

print("🧠 Initialisation du moteur de génération LLM (Qwen-0.5B-Chat)...")
generator_rag = pipeline("text-generation", model="Qwen/Qwen1.5-0.5B-Chat")
print("✅ Architecture RAG prête pour la production !")

# Schema de données conforme Pydantic v2
class DemandeRAG(BaseModel):
    query: str = Field(
        ..., 
        json_schema_extra={"example": "Quel est le revenu minimum pour obtenir un crédit ?"}
    )

# Base de connaissances interne de l'entreprise
base_connaissances = [
    "Les conditions d'octroi de crédit exigent un revenu mensuel minimum de 3000 euros et un ratio d'endettement inférieur à 33%.",
    "Pour la prédiction du churn client, l'équipe marketing utilise un modèle Random Forest basé sur l'ancienneté et les réclamations.",
    "L'aiguillage automatique des tickets NLP utilise l'algorithme Naive Bayes pour classifier la facturation et le support technique.",
    "La segmentation client s'appuie sur le clustering K-Means avec 4 profils distincts d'acheteurs."
]

# Vectorisation et indexation de la base de connaissances
vectorizer = TfidfVectorizer()
X_knowledge = vectorizer.fit_transform(base_connaissances)

# 2. Endpoint d'inférence RAG
@app.post("/ask_rag", summary="Interroger la base de connaissances avec validation LLM")
def interroger_rag(donnees: DemandeRAG):
    try:
        # --- PHASE 1 : RETRIEVAL (Extraction du contexte le plus proche) ---
        query_vector = vectorizer.transform([donnees.query])
        similarites = cosine_similarity(query_vector, X_knowledge).flatten()
        index_meilleur_contexte = int(np.argmax(similarites))
        score_pertinence = float(similarites[index_meilleur_contexte])
        
        # Filtrage défensif
        if score_pertinence < 0.15:
            contexte_retrouve = "Aucun document d'entreprise pertinent trouvé pour cette requête."
        else:
            contexte_retrouve = base_connaissances[index_meilleur_contexte]
            
        # --- PHASE 2 : CONTEXT-INFUSED GENERATION (Transformers v5 Struct) ---
        messages = [
            {
                "role": "user",
                "content": f"Basé uniquement sur ce document : '{contexte_retrouve}'. Réponds de manière précise à la question suivante : {donnees.query}"
            }
        ]
        
        outputs = generator_rag(messages, max_new_tokens=100, do_sample=False)
        reponse_generee = outputs["generated_text"][-1]["content"]
        
        return {
            "user_query": donnees.query,
            "retrieval_status": "SUCCESS" if score_pertinence >= 0.15 else "LOW_CONFIDENCE",
            "similarity_score": round(score_pertinence, 4),
            "context_extracted": contexte_retrouve,
            "llm_response": reponse_generee.strip()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'infrastructure RAG : {str(e)}")
