import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.linear_model import LogisticRegression

# 1. Initialisation de l'API pour le Pipeline 10
app = FastAPI(
    title="Pipeline 10 : Credit Scoring Microservice",
    description="API industrielle d'évaluation du risque de crédit basée sur une Régression Logistique.",
    version="1.0.0"
)

# 2. Validation Typage Défensif (Pydantic v2)
class DemandePret(BaseModel):
    client_id: str = Field(..., example="LOAN_TOGO_77")
    revenus_mensuels: float = Field(..., description="Revenus en milliers d'euros", example=4.5)
    ratio_endettement: float = Field(..., description="Pourcentage d'endettement", example=25.0)
    historique_incidents: int = Field(..., description="Nombre d'incidents de paiement passés (0 ou 1)", example=0)

# 3. Entraînement initial du modèle de Credit Scoring
# Simulation de données bancaires historiques
X_train = np.array([
    [5.0, 20.0, 0],  # Profil sain
    [1.5, 50.0, 1],  # Profil très risqué
    [3.0, 30.0, 0],  # Profil moyen sain
    [2.0, 40.0, 1]   # Profil moyen risqué
])
y_train = np.array([0, 1, 0, 1])  # 0 = Approuvé, 1 = Refusé

model_credit = LogisticRegression()
model_credit.fit(X_train, y_train)

# 4. Endpoint unique du pipeline
@app.post("/evaluate_loan", summary="Évaluer le risque d'un dossier de prêt")
def evaluer_demande_pret(demande: DemandePret):
    try:
        # Extraction et formatage des caractéristiques d'entrée
        features = [[
            demande.revenus_mensuels,
            demande.ratio_endettement,
            demande.historique_incidents
        ]]
        
        # Inférence Industrielle (Calcul des probabilités de défaut)
        prediction = int(model_credit.predict(features))
        probabilites = model_credit.predict_proba(features)
        probabilite_defaut = float(probabilites[0][1])
        
        # Logique métier décisionnelle bancaire
        if prediction == 0 and probabilite_defaut < 0.35:
            decision = "ACCEPTED 🟢"
            statut = "Dossier conforme aux critères d'octroi de crédit"
        else:
            decision = "REFUSED ❌"
            statut = "Niveau de risque supérieur au seuil de tolérance bancaire"
            
        return {
            "loan_application_id": demande.client_id,
            "status": "low_risk" if prediction == 0 else "high_risk",
            "default_probability": round(probabilite_defaut, 4),
            "credit_score_decision": f"{decision} ({statut})"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'inférence : {str(e)}")
