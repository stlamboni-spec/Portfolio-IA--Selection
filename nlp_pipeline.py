import math
from collections import Counter
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

# 1. Initialisation de l'application de Classification NLP
app = FastAPI(
    title="Statistical NLP Text Classifier",
    description="Analytics Pipeline: High-speed Multinomial Naïve Bayes baseline.",
    version="1.0.0"
)

class TextClassificationRequest(BaseModel):
    text: str = Field(..., min_length=3, description="Le texte ou message à classifier.")

class TextClassificationResponse(BaseModel):
    text: str
    predicted_category: str
    confidence_log_probability: float
    message: str

# --- ENTRAÎNEMENT SIMULÉ D'UN MODÈLE NAÏVE BAYES (Prior & Likelihood) ---
# Dictionnaires de fréquences de mots pour deux classes : SPAM et INBOX (Ham)
VOCABULARY_COUNTS = {
    "SPAM": {"gagner": 15, "gratuit": 20, "argent": 12, "offre": 10, "cliquer": 18},
    "INBOX": {"réunion": 14, "projet": 18, "code": 15, "rapport": 10, "merci": 22}
}

TOTAL_WORDS_PER_CLASS = {
    "SPAM": sum(VOCABULARY_COUNTS["SPAM"].values()),
    "INBOX": sum(VOCABULARY_COUNTS["INBOX"].values())
}

# Taille unique du vocabulaire global pour le lissage de Laplace (Laplace Smoothing)
V_SIZE = len(set(list(VOCABULARY_COUNTS["SPAM"].keys()) + list(VOCABULARY_COUNTS["INBOX"].keys())))

def predict_naive_bayes(text: str):
    """Calcule les probabilités a posteriori (log-likelihood) pour chaque classe."""
    words = text.lower().split()
    
    # Prior équitable (0.5 / 0.5) -> log(0.5)
    log_probs = {"SPAM": math.log(0.5), "INBOX": math.log(0.5)}
    
    for category in ["SPAM", "INBOX"]:
        for word in words:
            # Comptage du mot avec lissage de Laplace (+1)
            word_count = VOCABULARY_COUNTS[category].get(word, 0) + 1
            # Division par le total de la classe + taille du vocabulaire
            word_prob = word_count / (TOTAL_WORDS_PER_CLASS[category] + V_SIZE)
            # Accumulation en log pour éviter le sous-flux numérique (underflow)
            log_probs[category] += math.log(word_prob)
            
    # Sélection de la classe avec la probabilité maximale
    predicted_class = max(log_probs, key=log_probs.get)
    return predicted_class, log_probs[predicted_class]

# --- ENDPOINT API ---
@app.post("/api/v1/nlp/classify", response_model=TextClassificationResponse)
async def classify_incoming_text(request: TextClassificationRequest):
    """Analyse sémantique statistique ultra-rapide du texte entrant."""
    category, log_prob = predict_naive_bayes(request.text)
    
    return TextClassificationResponse(
        text=request.text,
        predicted_category=category,
        confidence_log_probability=round(log_prob, 3),
        message="Classification statistique Naïve Bayes complétée avec succès."
    )

# 2. Validation instantanée via TestClient
client = TestClient(app)

print("=== ENGIN STATISTIQUE NLP (NAÏVE BAYES MULTINOMIAL) ===")

# Scénarios de tests
textes_test = [
    "Gagner de l'argent gratuit avec cette offre exclusive cliquez",
    "Merci de m'envoyer le rapport de code pour le projet de réunion"
]

for idx, txt in enumerate(textes_test, 1):
    response = client.post("/api/v1/nlp/classify", json={"text": txt})
    res_data = response.json()
    print(f"\n[Test #{idx}] Texte analysé : '{res_data['text']}'")
    print(f"         -> Catégorie Prédite : {res_data['predicted_category']} (Log-Probabilité : {res_data['confidence_log_probability']})")

        
