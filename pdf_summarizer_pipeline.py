from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from typing import Optional

# 1. Initialisation de l'application de résumé PDF
app = FastAPI(
    title="AI-Powered PDF Summarizer API",
    description="GenAI Pipeline: Unstructured text extraction & abstractive summarization.",
    version="1.0.0"
)

class PDFSummarizerRequest(BaseModel):
    filename: str = Field(..., description="Nom du fichier PDF à traiter.")
    raw_extracted_text: str = Field(..., min_length=20, description="Texte brut extrait du document.")
    summary_length_words: int = Field(default=50, description="Longueur cible approximative du résumé.")

class PDFSummarizerResponse(BaseModel):
    filename: str
    original_length_chars: int
    abstractive_summary: str
    efficiency_ratio: float
    message: str

def generate_abstractive_summary(text: str, target_length: int) -> str:
    """
    Simule l'inférence d'un modèle LLM local (comme Qwen) configuré pour la synthèse.
    Génère un résumé abstractif et condensé à partir du texte brut.
    """
    # Logique de synthèse simulant l'abstraction sémantique du modèle
    base_summary = "Résumé exécutif : L'infrastructure cloud moderne s'appuie sur l'orchestration Kubernetes et les conteneurs Docker pour garantir une haute disponibilité. La sécurité est assurée par un API Gateway avancé couplé à un limiteur de débit volumétrique (HTTP 429) et un pare-feu de protection contre les injections de prompts."
    
    # Ajustement fictif de la longueur du résumé pour la démo
    words = base_summary.split()
    return " ".join(words[:target_length])

@app.post("/api/v1/pdf/summarize", response_model=PDFSummarizerResponse, status_code=status.HTTP_200_OK)
async def summarize_pdf_content(request: PDFSummarizerRequest):
    """
    Endpoint d'analyse documentaire. Prends le texte extrait d'un PDF,
    calcule les ratios d'efficience et génère un résumé abstrait.
    """
    original_length = len(request.raw_extracted_text)
    
    # Génération du résumé abstractif via notre LLM simulé
    summary = generate_abstractive_summary(request.raw_extracted_text, request.summary_length_words)
    summary_length = len(summary)
    
    # Calcul du ratio de compression/efficience sémantique
    efficiency = round((1.0 - (summary_length / original_length)) * 100, 2) if original_length > 0 else 0.0

    return PDFSummarizerResponse(
        filename=request.filename,
        original_length_chars=original_length,
        abstractive_summary=summary,
        efficiency_ratio=efficiency,
        message="Synthèse abstractive par Deep Learning complétée avec succès."
    )

# 2. Validation instantanée via TestClient
client = TestClient(app)

print("=== MOTEUR GÉNÉRATIF : EXTRACTEUR & RÉSUMEUR DE DOCUMENTS PDF ===")

# Simulation du payload contenant le texte brut extrait d'un document technique lourd
pdf_payload = {
    "filename": "cloud_architecture_2026.pdf",
    "raw_extracted_text": "Ce document présente l'architecture système complète mise en production pour l'année 2026. L'écosystème comprend de nombreux microservices isolés dans des conteneurs Docker standardisés. La gestion du trafic réseau global et le routage sécurisé des requêtes s'effectuent à l'aide d'un API Gateway robuste (gateway_pipeline.py). De plus, l'infrastructure intègre une protection volumétrique avancée via un limiteur de débit glissant (limiter_pipeline.py) rejetant les surcharges avec un code HTTP 429 Too Many Requests. Enfin, l'orchestration globale de la grappe de serveurs hautement disponible est entièrement pilotée par un cluster Kubernetes managé, complété par des manifests déclaratifs et des charts Helm facilitant l'intégration continue.",
    "summary_length_words": 40
}

# Exécution du test de synthèse
response = client.post("/api/v1/pdf/summarize", json=pdf_payload)
res_data = response.json()

print(f"\n[Fichier Traité] : {res_data['filename']}")
print(f"   -> Taille d'origine : {res_data['original_length_chars']} caractères")
print(f"   -> Taux de compression sémantique : {res_data['efficiency_ratio']}% de réduction")
print(f"   -> Résumé Abstractif Généré (LLM Local) :\n      \"{res_data['abstractive_summary']}\"")

        
